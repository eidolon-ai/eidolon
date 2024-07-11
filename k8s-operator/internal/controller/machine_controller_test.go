package controller

import (
	"context"
	serverv1alpha1 "github.com/eidolon-ai/eidolon/k8s-operator/api/v1alpha1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/kubernetes/scheme"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/yaml"
	"time"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
)

func createNamespaceIfNotExists(ctx context.Context, namespace string) error {
	ns := &corev1.Namespace{}
	err := k8sClient.Get(ctx, types.NamespacedName{Name: namespace}, ns)
	if err != nil && errors.IsNotFound(err) {
		ns = &corev1.Namespace{
			ObjectMeta: metav1.ObjectMeta{
				Name: namespace,
			},
		}
		err = k8sClient.Create(ctx, ns)
	}
	return err
}

var _ = Describe("Machine Controller", func() {
	const (
		MachineName      = "test-machine"
		MachineNamespace = "default"
		timeout          = time.Second * 10
		interval         = time.Millisecond * 250
	)

	var (
		mgr       ctrl.Manager
		mgrCtx    context.Context
		mgrCancel context.CancelFunc
	)

	BeforeEach(func() {
		ctx := context.Background()

		// Set up a new manager and controller for each test
		var err error
		mgr, err = ctrl.NewManager(cfg, ctrl.Options{
			Scheme: scheme.Scheme,
		})
		Expect(err).ToNot(HaveOccurred())

		Expect(createNamespaceIfNotExists(ctx, MachineNamespace)).To(Succeed())

		controller := &MachineReconciler{
			Client: mgr.GetClient(),
			Scheme: mgr.GetScheme(),
		}
		err = controller.SetupWithManager(mgr)
		Expect(err).ToNot(HaveOccurred())

		mgrCtx, mgrCancel = context.WithCancel(ctx)

		go func() {
			err := mgr.Start(mgrCtx)
			if err != nil {
				Expect(err).NotTo(HaveOccurred())
			}
		}()

		// Wait for the manager to be ready
		Expect(mgr.GetCache().WaitForCacheSync(mgrCtx)).To(BeTrue())
	})

	AfterEach(func() {
		// Stop the manager after each test
		mgrCancel()
		// You might want to add a small delay here to ensure the manager has stopped
		time.Sleep(100 * time.Millisecond)
	})

	Context("When creating a Machine", func() {
		It("Should create a Deployment and ConfigMap", func() {
			ctx := context.Background()

			machineYAML := `
apiVersion: server.eidolonai.com/v1alpha1
kind: Machine
metadata:
  name: test-machine
  namespace: default
spec:
  image: test-image:v1
  replicas: 1
  additionalField1: value1
  additionalField2:
    nestedField: nestedValue
`
			// Parse YAML into an unstructured object
			unstructuredObj := &unstructured.Unstructured{}
			err := yaml.Unmarshal([]byte(machineYAML), unstructuredObj)
			Expect(err).NotTo(HaveOccurred())

			// Verify the additional fields
			spec, found, err := unstructured.NestedMap(unstructuredObj.Object, "spec")
			Expect(err).NotTo(HaveOccurred())
			Expect(found).To(BeTrue())

			Expect(spec).To(HaveKeyWithValue("additionalField1", "value1"))
			Expect(spec).To(HaveKey("additionalField2"))
			additionalField2, ok := spec["additionalField2"].(map[string]interface{})
			Expect(ok).To(BeTrue())
			Expect(additionalField2).To(HaveKeyWithValue("nestedField", "nestedValue"))

			// Convert unstructured to Machine
			machine := &serverv1alpha1.Machine{}
			err = runtime.DefaultUnstructuredConverter.FromUnstructured(unstructuredObj.Object, machine)
			Expect(err).NotTo(HaveOccurred())

			// Create the Machine
			Expect(k8sClient.Create(ctx, machine)).Should(Succeed())

			deploymentLookupKey := types.NamespacedName{Name: "eidolon-deployment", Namespace: MachineNamespace}
			createdDeployment := &appsv1.Deployment{}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, deploymentLookupKey, createdDeployment)
				return err == nil
			}, timeout, interval).Should(BeTrue())
			Expect(*createdDeployment.Spec.Replicas).Should(Equal(int32(1)))
			Expect(createdDeployment.Spec.Template.Spec.Containers[0].Image).Should(Equal("test-image:v1"))

			configMapLookupKey := types.NamespacedName{Name: "eidolon-machine-cm", Namespace: MachineNamespace}
			createdConfigMap := &corev1.ConfigMap{}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, configMapLookupKey, createdConfigMap)
				return err == nil
			}, timeout, interval).Should(BeTrue())
			Expect(createdConfigMap.Data["machine.yaml"]).Should(ContainSubstring("nestedField: nestedValue"))
		})
		It("Should create a Service", func() {
			ctx := context.Background()

			serviceLookupKey := types.NamespacedName{Name: "eidolon-service", Namespace: MachineNamespace}
			createdService := &corev1.Service{}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, serviceLookupKey, createdService)
				return err == nil
			}, timeout, interval).Should(BeTrue())

			Expect(createdService.Spec.Ports).To(HaveLen(1))
			Expect(createdService.Spec.Ports[0].Port).To(Equal(int32(8080)))
			Expect(createdService.Spec.Selector).To(HaveKeyWithValue("app", "eidolon"))
		})
	})

	Context("When updating a Machine", func() {
		It("Should update the Deployment when scaling replicas", func() {
			ctx := context.Background()
			machine := &serverv1alpha1.Machine{}
			Expect(k8sClient.Get(ctx, types.NamespacedName{Name: MachineName, Namespace: MachineNamespace}, machine)).Should(Succeed())

			machine.Spec.Replicas = int32Ptr(3)
			Expect(k8sClient.Update(ctx, machine)).Should(Succeed())

			deploymentLookupKey := types.NamespacedName{Name: "eidolon-deployment", Namespace: MachineNamespace}
			updatedDeployment := &appsv1.Deployment{}
			Eventually(func() int32 {
				err := k8sClient.Get(ctx, deploymentLookupKey, updatedDeployment)
				if err != nil {
					return 0
				}
				return *updatedDeployment.Spec.Replicas
			}, timeout, interval).Should(Equal(int32(3)))
		})

		It("Should update the Deployment when changing image", func() {
			ctx := context.Background()
			machine := &serverv1alpha1.Machine{}
			Expect(k8sClient.Get(ctx, types.NamespacedName{Name: MachineName, Namespace: MachineNamespace}, machine)).Should(Succeed())

			machine.Spec.Image = "test-image:v2"
			Expect(k8sClient.Update(ctx, machine)).Should(Succeed())

			deploymentLookupKey := types.NamespacedName{Name: "eidolon-deployment", Namespace: MachineNamespace}
			updatedDeployment := &appsv1.Deployment{}
			Eventually(func() string {
				err := k8sClient.Get(ctx, deploymentLookupKey, updatedDeployment)
				if err != nil {
					return ""
				}
				return updatedDeployment.Spec.Template.Spec.Containers[0].Image
			}, timeout, interval).Should(Equal("test-image:v2"))
		})

		It("Should update the ConfigMap and bump deployment annotation when changing additional fields", func() {
			ctx := context.Background()

			updatedMachineYAML := `
apiVersion: server.eidolonai.com/v1alpha1
kind: Machine
metadata:
  name: test-machine
  namespace: default
spec:
  image: test-image:v2
  replicas: 2
  additionalField1: updatedValue1
  additionalField3: newValue
`

			updatedMachine := &serverv1alpha1.Machine{}
			err := yaml.Unmarshal([]byte(updatedMachineYAML), updatedMachine)
			Expect(err).NotTo(HaveOccurred())

			// Get the existing Machine
			existingMachine := &serverv1alpha1.Machine{}
			Expect(k8sClient.Get(ctx, types.NamespacedName{Name: MachineName, Namespace: MachineNamespace}, existingMachine)).Should(Succeed())

			// Update the existing Machine
			existingMachine.Spec = updatedMachine.Spec
			Expect(k8sClient.Update(ctx, existingMachine)).Should(Succeed())

			// Check if the Deployment was updated
			updatedDeployment := &appsv1.Deployment{}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, types.NamespacedName{Name: "eidolon-deployment", Namespace: MachineNamespace}, updatedDeployment)
				if err != nil {
					return false
				}
				return *updatedDeployment.Spec.Replicas == int32(2) &&
					updatedDeployment.Spec.Template.Spec.Containers[0].Image == "test-image:v2"
			}, timeout, interval).Should(BeTrue())

			// Check if the ConfigMap was updated
			updatedConfigMap := &corev1.ConfigMap{}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, types.NamespacedName{Name: "eidolon-machine-cm", Namespace: MachineNamespace}, updatedConfigMap)
				if err != nil {
					return false
				}
				return updatedConfigMap.Data["machine.yaml"] != ""
			}, timeout, interval).Should(BeTrue())
			Expect(updatedConfigMap.Data["machine.yaml"]).Should(ContainSubstring("additionalField1: updatedValue1"))
			Expect(updatedConfigMap.Data["machine.yaml"]).Should(ContainSubstring("additionalField3: newValue"))
			Expect(updatedConfigMap.Data["machine.yaml"]).ShouldNot(ContainSubstring("additionalField2:"))
			Expect(updatedDeployment.Spec.Template.ObjectMeta.Annotations["machine-cm-version"]).Should(Equal(updatedConfigMap.ResourceVersion))
		})
	})

	Context("When external ConfigMaps change", func() {
		It("Should update the Deployment when agent ConfigMap changes", func() {
			ctx := context.Background()
			agentCM := &corev1.ConfigMap{
				ObjectMeta: metav1.ObjectMeta{
					Name:      "eidolon-agent-cm",
					Namespace: MachineNamespace,
				},
				Data: map[string]string{
					"agents.yaml": "initial: data",
				},
			}
			Expect(k8sClient.Create(ctx, agentCM)).Should(Succeed())

			// Wait for the Deployment to be updated with the agent ConfigMap
			deploymentLookupKey := types.NamespacedName{Name: "eidolon-deployment", Namespace: MachineNamespace}
			updatedDeployment := &appsv1.Deployment{}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, deploymentLookupKey, updatedDeployment)
				if err != nil {
					return false
				}
				return updatedDeployment.Spec.Template.ObjectMeta.Annotations["agent-cm-version"] != ""
			}, timeout, interval).Should(BeTrue())

			// Update the agent ConfigMap
			agentCM.Data["agents.yaml"] = "updated: data"
			Expect(k8sClient.Update(ctx, agentCM)).Should(Succeed())

			// Check if the Deployment is updated with the new ConfigMap version
			Eventually(func() string {
				err := k8sClient.Get(ctx, deploymentLookupKey, updatedDeployment)
				if err != nil {
					return ""
				}
				return updatedDeployment.Spec.Template.ObjectMeta.Annotations["agent-cm-version"]
			}, timeout, interval).Should(Equal(agentCM.ResourceVersion))
		})

		It("Should update the Deployment when reference ConfigMap changes", func() {
			ctx := context.Background()
			referenceCM := &corev1.ConfigMap{
				ObjectMeta: metav1.ObjectMeta{
					Name:      "eidolon-reference-cm",
					Namespace: MachineNamespace,
				},
				Data: map[string]string{
					"references.yaml": "initial: data",
				},
			}
			Expect(k8sClient.Create(ctx, referenceCM)).Should(Succeed())

			// Wait for the Deployment to be updated with the reference ConfigMap
			deploymentLookupKey := types.NamespacedName{Name: "eidolon-deployment", Namespace: MachineNamespace}
			updatedDeployment := &appsv1.Deployment{}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, deploymentLookupKey, updatedDeployment)
				if err != nil {
					return false
				}
				return updatedDeployment.Spec.Template.ObjectMeta.Annotations["reference-cm-version"] != ""
			}, timeout, interval).Should(BeTrue())

			// Update the reference ConfigMap
			referenceCM.Data["references.yaml"] = "updated: data"
			Expect(k8sClient.Update(ctx, referenceCM)).Should(Succeed())

			// Check if the Deployment is updated with the new ConfigMap version
			Eventually(func() string {
				err := k8sClient.Get(ctx, deploymentLookupKey, updatedDeployment)
				if err != nil {
					return ""
				}
				return updatedDeployment.Spec.Template.ObjectMeta.Annotations["reference-cm-version"]
			}, timeout, interval).Should(Equal(referenceCM.ResourceVersion))
		})
	})

	Context("When deleting a Machine", func() {
		It("Should delete the Deployment and ConfigMap", func() {
			ctx := context.Background()
			machine := &serverv1alpha1.Machine{}
			Expect(k8sClient.Get(ctx, types.NamespacedName{Name: MachineName, Namespace: MachineNamespace}, machine)).Should(Succeed())

			Expect(k8sClient.Delete(ctx, machine)).Should(Succeed())

			serviceLookupKey := types.NamespacedName{Name: "eidolon-service", Namespace: MachineNamespace}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, serviceLookupKey, &corev1.Service{})
				return errors.IsNotFound(err)
			}, timeout, interval).Should(BeTrue())

			deploymentLookupKey := types.NamespacedName{Name: "eidolon-deployment", Namespace: MachineNamespace}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, deploymentLookupKey, &appsv1.Deployment{})
				return errors.IsNotFound(err)
			}, timeout, interval).Should(BeTrue())

			configMapLookupKey := types.NamespacedName{Name: "eidolon-machine-cm", Namespace: MachineNamespace}
			Eventually(func() bool {
				err := k8sClient.Get(ctx, configMapLookupKey, &corev1.ConfigMap{})
				return errors.IsNotFound(err)
			}, timeout, interval).Should(BeTrue())
		})
	})
})

func int32Ptr(i int32) *int32 { return &i }

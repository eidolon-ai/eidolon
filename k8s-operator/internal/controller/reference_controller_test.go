package controller

import (
	"gopkg.in/yaml.v3"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"

	"context"
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"

	serverv1alpha1 "github.com/eidolon-ai/eidolon/k8s-operator/api/v1alpha1"
)

var _ = Describe("Reference Reconciler", func() {
	Context("When reconciling References", func() {
		const (
			referenceName = "test-reference"
			namespace     = "default"
			configMapName = "eidolon-reference-cm"
		)

		ctx := context.Background()
		typeNamespacedName := types.NamespacedName{
			Name:      referenceName,
			Namespace: namespace,
		}

		BeforeEach(func() {
			// Create a test Reference
			reference := &serverv1alpha1.Reference{
				ObjectMeta: metav1.ObjectMeta{
					Name:      referenceName,
					Namespace: namespace,
				},
				Spec: serverv1alpha1.ReferenceSpec{
					RawExtension: runtime.RawExtension{
						Raw: []byte(`{"implementation": "TestReference"}`),
					},
				},
			}
			Expect(k8sClient.Create(ctx, reference)).To(Succeed())
		})

		AfterEach(func() {
			// Cleanup
			reference := &serverv1alpha1.Reference{}
			err := k8sClient.Get(ctx, typeNamespacedName, reference)
			if err == nil {
				Expect(k8sClient.Delete(ctx, reference)).To(Succeed())
			}

			configMap := &corev1.ConfigMap{}
			err = k8sClient.Get(ctx, types.NamespacedName{Name: configMapName, Namespace: namespace}, configMap)
			if err == nil {
				Expect(k8sClient.Delete(ctx, configMap)).To(Succeed())
			}
		})

		It("should create a ConfigMap when an Reference is created", func() {
			reconciler := &ReferenceReconciler{
				Client: k8sClient,
				Scheme: k8sClient.Scheme(),
			}

			_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Check if ConfigMap was created
			configMap := &corev1.ConfigMap{}
			err = k8sClient.Get(ctx, types.NamespacedName{Name: configMapName, Namespace: namespace}, configMap)
			Expect(err).NotTo(HaveOccurred())

			// Verify ConfigMap content
			Expect(configMap.Data).To(HaveKey("references.yaml"))
			yamlContent := configMap.Data["references.yaml"]

			var parsedYAML map[string]interface{}
			err = yaml.Unmarshal([]byte(yamlContent), &parsedYAML)
			Expect(err).NotTo(HaveOccurred())

			spec, ok := parsedYAML["spec"].(map[string]interface{})
			Expect(ok).To(BeTrue())
			Expect(spec).To(HaveKey("implementation"))
			Expect(spec["implementation"]).To(Equal("TestReference"))
		})

		It("should update the ConfigMap when an Reference is updated", func() {
			reconciler := &ReferenceReconciler{
				Client: k8sClient,
				Scheme: k8sClient.Scheme(),
			}

			// Initial reconciliation
			_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Update the Reference
			reference := &serverv1alpha1.Reference{}
			Expect(k8sClient.Get(ctx, typeNamespacedName, reference)).To(Succeed())
			reference.Spec.RawExtension = runtime.RawExtension{
				Raw: []byte(`{"implementation": "UpdatedTestReference"}`),
			}

			Expect(k8sClient.Update(ctx, reference)).To(Succeed())

			// Reconcile again
			_, err = reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Check if ConfigMap was updated
			configMap := &corev1.ConfigMap{}
			err = k8sClient.Get(ctx, types.NamespacedName{Name: configMapName, Namespace: namespace}, configMap)
			Expect(err).NotTo(HaveOccurred())

			// Verify updated ConfigMap content
			Expect(configMap.Data).To(HaveKey("references.yaml"))
			yamlContent := configMap.Data["references.yaml"]
			var parsedYAML map[string]interface{}
			err = yaml.Unmarshal([]byte(yamlContent), &parsedYAML)
			Expect(err).NotTo(HaveOccurred())

			spec, ok := parsedYAML["spec"].(map[string]interface{})
			Expect(ok).To(BeTrue())
			Expect(spec).To(HaveKey("implementation"))
			Expect(spec["implementation"]).To(Equal("UpdatedTestReference"))
		})

		It("should remove an Reference from the ConfigMap when it's deleted", func() {
			reconciler := &ReferenceReconciler{
				Client: k8sClient,
				Scheme: k8sClient.Scheme(),
			}

			// Initial reconciliation
			_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Delete the Reference
			reference := &serverv1alpha1.Reference{}
			Expect(k8sClient.Get(ctx, typeNamespacedName, reference)).To(Succeed())
			Expect(k8sClient.Delete(ctx, reference)).To(Succeed())

			// Reconcile again
			_, err = reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Check if Reference was removed from ConfigMap
			configMap := &corev1.ConfigMap{}
			err = k8sClient.Get(ctx, types.NamespacedName{Name: configMapName, Namespace: namespace}, configMap)
			Expect(err).NotTo(HaveOccurred())

			// Verify ConfigMap content
			Expect(configMap.Data).To(HaveKey("references.yaml"))
			yamlContent := configMap.Data["references.yaml"]
			Expect(yamlContent).NotTo(ContainSubstring(referenceName))
		})
	})
})

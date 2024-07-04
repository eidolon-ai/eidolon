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

var ctx context.Context

var _ = Describe("Agent Reconciler", func() {
	Context("When reconciling Agents", func() {
		const (
			agentName     = "test-agent"
			namespace     = "default"
			configMapName = "eidolon-agent-cm"
		)

		ctx := context.Background()
		typeNamespacedName := types.NamespacedName{
			Name:      agentName,
			Namespace: namespace,
		}

		BeforeEach(func() {
			// Create a test Agent
			agent := &serverv1alpha1.Agent{
				ObjectMeta: metav1.ObjectMeta{
					Name:      agentName,
					Namespace: namespace,
				},
				Spec: serverv1alpha1.AgentSpec{
					RawExtension: runtime.RawExtension{
						Raw: []byte(`{"implementation": "TestAgent"}`),
					},
				},
			}
			Expect(k8sClient.Create(ctx, agent)).To(Succeed())
		})

		AfterEach(func() {
			// Cleanup
			agent := &serverv1alpha1.Agent{}
			err := k8sClient.Get(ctx, typeNamespacedName, agent)
			if err == nil {
				Expect(k8sClient.Delete(ctx, agent)).To(Succeed())
			}

			configMap := &corev1.ConfigMap{}
			err = k8sClient.Get(ctx, types.NamespacedName{Name: configMapName, Namespace: namespace}, configMap)
			if err == nil {
				Expect(k8sClient.Delete(ctx, configMap)).To(Succeed())
			}
		})

		It("should create a ConfigMap when an Agent is created", func() {
			reconciler := &AgentReconciler{
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
			Expect(configMap.Data).To(HaveKey("agents.yaml"))
			yamlContent := configMap.Data["agents.yaml"]

			var parsedYAML map[string]interface{}
			err = yaml.Unmarshal([]byte(yamlContent), &parsedYAML)
			Expect(err).NotTo(HaveOccurred())

			spec, ok := parsedYAML["spec"].(map[string]interface{})
			Expect(ok).To(BeTrue())
			Expect(spec).To(HaveKey("implementation"))
			Expect(spec["implementation"]).To(Equal("TestAgent"))
		})

		It("should update the ConfigMap when an Agent is updated", func() {
			reconciler := &AgentReconciler{
				Client: k8sClient,
				Scheme: k8sClient.Scheme(),
			}

			// Initial reconciliation
			_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Update the Agent
			agent := &serverv1alpha1.Agent{}
			Expect(k8sClient.Get(ctx, typeNamespacedName, agent)).To(Succeed())
			agent.Spec.RawExtension = runtime.RawExtension{
				Raw: []byte(`{"implementation": "UpdatedTestAgent"}`),
			}

			Expect(k8sClient.Update(ctx, agent)).To(Succeed())

			// Reconcile again
			_, err = reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Check if ConfigMap was updated
			configMap := &corev1.ConfigMap{}
			err = k8sClient.Get(ctx, types.NamespacedName{Name: configMapName, Namespace: namespace}, configMap)
			Expect(err).NotTo(HaveOccurred())

			// Verify updated ConfigMap content
			Expect(configMap.Data).To(HaveKey("agents.yaml"))
			yamlContent := configMap.Data["agents.yaml"]
			var parsedYAML map[string]interface{}
			err = yaml.Unmarshal([]byte(yamlContent), &parsedYAML)
			Expect(err).NotTo(HaveOccurred())

			spec, ok := parsedYAML["spec"].(map[string]interface{})
			Expect(ok).To(BeTrue())
			Expect(spec).To(HaveKey("implementation"))
			Expect(spec["implementation"]).To(Equal("UpdatedTestAgent"))
		})

		It("should remove an Agent from the ConfigMap when it's deleted", func() {
			reconciler := &AgentReconciler{
				Client: k8sClient,
				Scheme: k8sClient.Scheme(),
			}

			// Initial reconciliation
			_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Delete the Agent
			agent := &serverv1alpha1.Agent{}
			Expect(k8sClient.Get(ctx, typeNamespacedName, agent)).To(Succeed())
			Expect(k8sClient.Delete(ctx, agent)).To(Succeed())

			// Reconcile again
			_, err = reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
			Expect(err).NotTo(HaveOccurred())

			// Check if Agent was removed from ConfigMap
			configMap := &corev1.ConfigMap{}
			err = k8sClient.Get(ctx, types.NamespacedName{Name: configMapName, Namespace: namespace}, configMap)
			Expect(err).NotTo(HaveOccurred())

			// Verify ConfigMap content
			Expect(configMap.Data).To(HaveKey("agents.yaml"))
			yamlContent := configMap.Data["agents.yaml"]
			Expect(yamlContent).NotTo(ContainSubstring(agentName))
		})
	})
})

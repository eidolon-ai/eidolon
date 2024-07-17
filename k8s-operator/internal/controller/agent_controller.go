/*
Copyright 2024.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"gopkg.in/yaml.v3"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/apimachinery/pkg/util/json"
	"strings"

	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/log"

	serverv1alpha1 "github.com/eidolon-ai/eidolon/k8s-operator/api/v1alpha1"
)

// AgentReconciler reconciles a Agent object
type AgentReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

func (r *AgentReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	// Fetch the Agent instance
	agent := &serverv1alpha1.Agent{}
	err := r.Get(ctx, req.NamespacedName, agent)
	if err != nil {
		if errors.IsNotFound(err) {
			// The Agent was deleted, we need to update the ConfigMap
			return r.updateConfigMap(ctx)
		}
		logger.Error(err, "Unable to fetch Agent")
		return ctrl.Result{}, err
	}

	// Update the ConfigMap with all Agents
	return r.updateConfigMap(ctx)
}

func (r *AgentReconciler) updateConfigMap(ctx context.Context) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	// List all Agents
	agentList := &serverv1alpha1.AgentList{}
	if err := r.List(ctx, agentList); err != nil {
		logger.Error(err, "Unable to list Agents")
		return ctrl.Result{}, err
	}

	// Concatenate all Agents into a single YAML string
	var agentsYAML strings.Builder
	for _, agent := range agentList.Items {
		// Convert the Agent to an unstructured object
		unstructuredObj, err := runtime.DefaultUnstructuredConverter.ToUnstructured(&agent)
		if err != nil {
			logger.Error(err, "Failed to convert Agent to unstructured", "Agent", agent.Name)
			continue
		}

		// Handle the RawExtension in the spec
		if spec, ok := unstructuredObj["spec"].(map[string]interface{}); ok {
			if rawExt, ok := spec["rawExtension"].(map[string]interface{}); ok {
				if raw, ok := rawExt["raw"].([]byte); ok {
					var specData interface{}
					if err := json.Unmarshal(raw, &specData); err == nil {
						spec["rawExtension"] = specData
					}
				}
			}
		}

		// Convert the unstructured object to YAML
		agentYAML, err := yaml.Marshal(unstructuredObj)
		if err != nil {
			logger.Error(err, "Failed to marshal Agent to YAML", "Agent", agent.Name)
			continue
		}
		agentsYAML.WriteString("---\n")
		agentsYAML.Write(agentYAML)
		agentsYAML.WriteString("\n")
	}

	// Define or update the ConfigMap
	cm := &corev1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name:      "eidolon-agent-cm",
			Namespace: "default", // You might want to make this configurable
		},
		Data: map[string]string{
			"agents.yaml": agentsYAML.String(),
		},
	}
	// Create or update the ConfigMap
	foundCM := &corev1.ConfigMap{}
	err := r.Get(ctx, types.NamespacedName{Name: cm.Name, Namespace: cm.Namespace}, foundCM)
	if err != nil && errors.IsNotFound(err) {
		logger.Info("Creating ConfigMap", "Name", cm.Name)
		err = r.Create(ctx, cm)
		if err != nil {
			logger.Error(err, "Failed to create ConfigMap")
			return ctrl.Result{}, err
		}
	} else if err != nil {
		logger.Error(err, "Failed to get ConfigMap")
		return ctrl.Result{}, err
	} else {
		// Update the existing ConfigMap
		foundCM.Data = cm.Data
		logger.Info("Updating ConfigMap", "Name", cm.Name)
		err = r.Update(ctx, foundCM)
		if err != nil {
			logger.Error(err, "Failed to update ConfigMap")
			return ctrl.Result{}, err
		}
	}

	return ctrl.Result{}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *AgentReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&serverv1alpha1.Agent{}).
		Owns(&corev1.ConfigMap{}).
		Complete(r)
}

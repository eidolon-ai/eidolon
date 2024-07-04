package controller

import (
	"context"
	"fmt"
	serverv1alpha1 "github.com/eidolon-ai/eidolon/k8s-operator/api/v1alpha1"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/builder"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/handler"
	"sigs.k8s.io/controller-runtime/pkg/log"
	"sigs.k8s.io/controller-runtime/pkg/predicate"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"
	"sigs.k8s.io/yaml"
)

type MachineReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

func (r *MachineReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	machine := &serverv1alpha1.Machine{}

    err := r.Get(ctx, req.NamespacedName, machine)
    if err != nil {
        if client.IgnoreNotFound(err) != nil {
            logger.Error(err, "Unable to fetch Machine")
            return ctrl.Result{}, err
        }
        // Machine resource not found, likely already deleted
        return ctrl.Result{}, nil
    }

    // Check if the Machine is being deleted
    if !machine.ObjectMeta.DeletionTimestamp.IsZero() {
        return r.handleDeletion(ctx, machine)
    }

    // Add finalizer if it doesn't exist
    if !controllerutil.ContainsFinalizer(machine, machineFinalizer) {
        controllerutil.AddFinalizer(machine, machineFinalizer)
        err = r.Update(ctx, machine)
        if err != nil {
            return ctrl.Result{}, err
        }
    }

	// Create or update the ConfigMap for additional fields
	if err := r.reconcileConfigMap(ctx, machine); err != nil {
		return ctrl.Result{}, err
	}

	// Create or update the Deployment
	if err := r.reconcileDeployment(ctx, machine); err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{}, nil
}

func (r *MachineReconciler) reconcileConfigMap(ctx context.Context, machine *serverv1alpha1.Machine) error {
	cm := &corev1.ConfigMap{}
	cm.Name = fmt.Sprintf("%s-machine-cm", machine.Name)
	cm.Namespace = machine.Namespace

	op, err := ctrl.CreateOrUpdate(ctx, r.Client, cm, func() error {
		if cm.Data == nil {
			cm.Data = make(map[string]string)
		}

		// convert machine into a map
		machineMap := make(map[string]interface{})
		machineBytes, _ := yaml.Marshal(machine)
		err := yaml.Unmarshal(machineBytes, &machineMap)

		if err != nil {
			return err
		}

		// Extract additional fields
		additionalFields, err := extractAdditionalFields(machine.Spec)
		if err != nil {
			return err
		}

		machineMap["Spec"] = additionalFields

		// Remove extra fields
		delete(machineMap, "status")
		delete(machineMap["metadata"].(map[string]interface{}), "managedFields")

		// Convert to YAML
		additionalYaml, err := yaml.Marshal(machineMap)
		if err != nil {
			return err
		}
		cm.Data["machine.yaml"] = string(additionalYaml)

		return controllerutil.SetControllerReference(machine, cm, r.Scheme)
	})

	if err != nil {
		return err
	}

	log.FromContext(ctx).Info("ConfigMap reconciled", "operation", op)
	return nil
}

func extractAdditionalFields(spec serverv1alpha1.MachineSpec) (map[string]interface{}, error) {
	// Convert spec to map
	specMap := make(map[string]interface{})
	specBytes, _ := yaml.Marshal(spec)
	err := yaml.Unmarshal(specBytes, &specMap)
	if err != nil {
		return nil, err
	}
	return specMap["AdditionalFields"].(map[string]interface{}), nil
}

func (r *MachineReconciler) reconcileDeployment(ctx context.Context, machine *serverv1alpha1.Machine) error {
	deploy := &appsv1.Deployment{}
	deploy.Name = fmt.Sprintf("%s-deployment", machine.Name)
	deploy.Namespace = machine.Namespace

	op, err := ctrl.CreateOrUpdate(ctx, r.Client, deploy, func() error {
		volumes := []corev1.Volume{
			{
				Name: "machine-config",
				VolumeSource: corev1.VolumeSource{
					ConfigMap: &corev1.ConfigMapVolumeSource{
						LocalObjectReference: corev1.LocalObjectReference{
							Name: fmt.Sprintf("%s-machine-cm", machine.Name),
						},
					},
				},
			},
		}

		volumeMounts := []corev1.VolumeMount{
			{
				Name:      "machine-config",
				MountPath: "/etc/eidolon/resources/machine",
			},
		}

		// Check and add agent config if it exists
		if r.configMapExists(ctx, "eidolon-agent-cm", machine.Namespace) {
			volumes = append(volumes, corev1.Volume{
				Name: "agent-config",
				VolumeSource: corev1.VolumeSource{
					ConfigMap: &corev1.ConfigMapVolumeSource{
						LocalObjectReference: corev1.LocalObjectReference{
							Name: "eidolon-agent-cm",
						},
					},
				},
			})
			volumeMounts = append(volumeMounts, corev1.VolumeMount{
				Name:      "agent-config",
				MountPath: "/etc/eidolon/resources/agents",
			})
		}

		// Check and add reference config if it exists
		if r.configMapExists(ctx, "eidolon-reference-cm", machine.Namespace) {
			volumes = append(volumes, corev1.Volume{
				Name: "reference-config",
				VolumeSource: corev1.VolumeSource{
					ConfigMap: &corev1.ConfigMapVolumeSource{
						LocalObjectReference: corev1.LocalObjectReference{
							Name: "eidolon-reference-cm",
						},
					},
				},
			})
			volumeMounts = append(volumeMounts, corev1.VolumeMount{
				Name:      "reference-config",
				MountPath: "/etc/eidolon/resources/references",
			})
		}

		deploy.Spec = appsv1.DeploymentSpec{
			Replicas: machine.Spec.Replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: map[string]string{"app": machine.Name},
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{"app": machine.Name},
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:         "eidolon-server",
							Image:        machine.Spec.Image,
							EnvFrom:      machine.Spec.EnvFrom,
							Ports:        machine.Spec.Ports,
							VolumeMounts: volumeMounts,
							Args:         r.generateArgs(ctx, machine),
						},
					},
					Volumes: volumes,
				},
			},
		}

		// Add ConfigMap versions to annotations
		annotations := map[string]string{}
		if agentCM, err := r.getConfigMap(ctx, "eidolon-agent-cm", machine.Namespace); err == nil {
			annotations["agent-cm-version"] = agentCM.ResourceVersion
		}
		if referenceCM, err := r.getConfigMap(ctx, "eidolon-reference-cm", machine.Namespace); err == nil {
			annotations["reference-cm-version"] = referenceCM.ResourceVersion
		}

		deploy.Spec.Template.ObjectMeta.Annotations = annotations

		return controllerutil.SetControllerReference(machine, deploy, r.Scheme)
	})

	if err != nil {
		return err
	}

	log.FromContext(ctx).Info("Deployment reconciled", "operation", op)
	return nil
}

func (r *MachineReconciler) getConfigMap(ctx context.Context, name, namespace string) (*corev1.ConfigMap, error) {
	cm := &corev1.ConfigMap{}
	err := r.Get(ctx, types.NamespacedName{Name: name, Namespace: namespace}, cm)
	return cm, err
}

func (r *MachineReconciler) generateArgs(ctx context.Context, machine *serverv1alpha1.Machine) []string {
	args := []string{"/etc/eidolon/resources/machine/machine.yaml"}

	if r.configMapExists(ctx, "eidolon-agent-cm", machine.Namespace) {
		args = append(args, "/etc/eidolon/resources/agents/agent.yaml")
	}

	if r.configMapExists(ctx, "eidolon-reference-cm", machine.Namespace) {
		args = append(args, "/etc/eidolon/resources/references/references.yaml")
	}

	return args
}

func (r *MachineReconciler) configMapExists(ctx context.Context, name, namespace string) bool {
	cm := &corev1.ConfigMap{}
	err := r.Get(ctx, types.NamespacedName{Name: name, Namespace: namespace}, cm)
	return err == nil
}

const machineFinalizer = "server.eidolon.ai/finalizer"

func (r *MachineReconciler) handleDeletion(ctx context.Context, machine *serverv1alpha1.Machine) (ctrl.Result, error) {
    logger := log.FromContext(ctx)

    // Check if the Machine has our finalizer
    if !controllerutil.ContainsFinalizer(machine, machineFinalizer) {
        // Our finalizer is not present, so the Machine can be deleted
        return ctrl.Result{}, nil
    }

    // Perform cleanup
    if err := r.deleteConfigMap(ctx, machine); err != nil {
        logger.Error(err, "Failed to delete ConfigMap")
        return ctrl.Result{}, err
    }

    if err := r.deleteDeployment(ctx, machine); err != nil {
        logger.Error(err, "Failed to delete Deployment")
        return ctrl.Result{}, err
    }

    // Remove our finalizer from the list and update it
    controllerutil.RemoveFinalizer(machine, machineFinalizer)
    if err := r.Update(ctx, machine); err != nil {
        return ctrl.Result{}, err
    }

    logger.Info("Successfully deleted Machine")
    return ctrl.Result{}, nil
}

func (r *MachineReconciler) deleteConfigMap(ctx context.Context, machine *serverv1alpha1.Machine) error {
    cm := &corev1.ConfigMap{
        ObjectMeta: metav1.ObjectMeta{
            Name:      fmt.Sprintf("%s-machine-cm", machine.Name),
            Namespace: machine.Namespace,
        },
    }
    return client.IgnoreNotFound(r.Delete(ctx, cm))
}

func (r *MachineReconciler) deleteDeployment(ctx context.Context, machine *serverv1alpha1.Machine) error {
    deploy := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      fmt.Sprintf("%s-deployment", machine.Name),
            Namespace: machine.Namespace,
        },
    }
    return client.IgnoreNotFound(r.Delete(ctx, deploy))
}

func (r *MachineReconciler) SetupWithManager(mgr ctrl.Manager) error {
	// Create a function to map ConfigMap changes to Machine reconcile requests
	mapConfigMapToMachine := func(ctx context.Context, obj client.Object) []reconcile.Request {
		configMap := obj.(*corev1.ConfigMap)
		machines := &serverv1alpha1.MachineList{}
		if err := r.List(ctx, machines, client.InNamespace(configMap.Namespace)); err != nil {
			return nil
		}

		var requests []reconcile.Request
		for _, machine := range machines.Items {
			requests = append(requests, reconcile.Request{
				NamespacedName: types.NamespacedName{
					Name:      machine.Name,
					Namespace: machine.Namespace,
				},
			})
		}
		return requests
	}

	return ctrl.NewControllerManagedBy(mgr).
		For(&serverv1alpha1.Machine{}).
		Owns(&corev1.ConfigMap{}). // For the machine-specific ConfigMap
		Owns(&appsv1.Deployment{}).
		Watches(
			&corev1.ConfigMap{},
			handler.EnqueueRequestsFromMapFunc(mapConfigMapToMachine),
			builder.WithPredicates(predicate.ResourceVersionChangedPredicate{}),
		).
		Complete(r)
}

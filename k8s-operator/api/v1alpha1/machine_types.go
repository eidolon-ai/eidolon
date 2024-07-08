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

package v1alpha1

import (
	"encoding/json"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
)

// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// MachineSpec defines the desired state of Machine
type MachineSpec struct {
	// Image is the container image to use for the Machine
	Image string `json:"image"`

	// Image pull policy.
	// One of Always, Never, IfNotPresent.
	// Defaults to Always if :latest tag is specified, or IfNotPresent otherwise.
	// Cannot be updated.
	// More info: https://kubernetes.io/docs/concepts/containers/images#updating-images
	// +optional
	ImagePullPolicy corev1.PullPolicy `json:"imagePullPolicy,omitempty" protobuf:"bytes,14,opt,name=imagePullPolicy,casttype=PullPolicy"`

	// SecurityContext holds pod-level security attributes and common container settings.
	// Optional: Defaults to empty.  See type description for default values of each field.
	// +optional
	SecurityContext *corev1.PodSecurityContext `json:"securityContext,omitempty" protobuf:"bytes,14,opt,name=securityContext"`

	// ImagePullSecrets is a list of references to secrets in the same namespace to use for pulling any images
	// in pods that reference this ServiceAccount. ImagePullSecrets are distinct from Secrets because Secrets
	// can be mounted in the pod, but ImagePullSecrets are only accessed by the kubelet.
	// More info: https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod
	// +optional
	ImagePullSecrets []corev1.LocalObjectReference `json:"imagePullSecrets,omitempty" protobuf:"bytes,3,rep,name=imagePullSecrets"`

	// Replicas is the number of desired replicas
	// +optional
	Replicas *int32 `json:"replicas,omitempty"`

	// Resources specifies the compute resources required by the container
	// +optional
	Resources corev1.ResourceRequirements `json:"resources,omitempty"`

	// Env is a list of environment variables to set in the container
	// +optional
	Env []corev1.EnvVar `json:"env,omitempty"`

	// EnvFrom is a list of sources to populate environment variables in the container
	// +optional
	EnvFrom []corev1.EnvFromSource `json:"envFrom,omitempty"`

	// Ports is a list of ports to expose from the container
	// +optional
	Ports []corev1.ContainerPort `json:"ports,omitempty"`

	// AdditionalVolumes allows specifying additional volumes to be mounted
	// +optional
	AdditionalVolumes []corev1.Volume `json:"additionalVolumes,omitempty"`

	// AdditionalVolumeMounts allows specifying additional volume mounts
	// +optional
	AdditionalVolumeMounts []corev1.VolumeMount `json:"additionalVolumeMounts,omitempty"`

	// ... other fields ...
	AdditionalFields runtime.RawExtension `json:",inline"`
}

func (in *MachineSpec) UnmarshalJSON(data []byte) error {
	// Create a type alias to avoid recursive calls to UnmarshalJSON
	type MachineSpecAlias MachineSpec

	// Create a temporary struct with MachineSpecAlias and a map for additional fields
	temp := struct {
		*MachineSpecAlias
		AdditionalFields map[string]interface{} `json:"-"`
	}{
		MachineSpecAlias: (*MachineSpecAlias)(in),
		AdditionalFields: make(map[string]interface{}),
	}

	// Unmarshal data into the temporary struct
	if err := json.Unmarshal(data, &temp); err != nil {
		return err
	}

	// Unmarshal data into the AdditionalFields map
	if err := json.Unmarshal(data, &temp.AdditionalFields); err != nil {
		return err
	}

	// Remove known fields
	delete(temp.AdditionalFields, "image")
	delete(temp.AdditionalFields, "replicas")
	delete(temp.AdditionalFields, "resources")
	delete(temp.AdditionalFields, "env")
	delete(temp.AdditionalFields, "envFrom")
	delete(temp.AdditionalFields, "ports")
	delete(temp.AdditionalFields, "additionalVolumes")
	delete(temp.AdditionalFields, "additionalVolumeMounts")

	// Marshal remaining fields into AdditionalFields
	if len(temp.AdditionalFields) > 0 {
		additionalFieldsData, err := json.Marshal(temp.AdditionalFields)
		if err != nil {
			return err
		}
		in.AdditionalFields = runtime.RawExtension{Raw: additionalFieldsData}
	}

	return nil
}

func (in *MachineSpec) MarshalJSON() ([]byte, error) {
	// Convert the MachineSpec to a map
	specMap := make(map[string]interface{})

	// Marshal the MachineSpec to JSON, then unmarshal to a map to get all fields
	specData, err := json.Marshal(*in)
	if err != nil {
		return nil, err
	}
	if err := json.Unmarshal(specData, &specMap); err != nil {
		return nil, err
	}

	// If there are additional fields, unmarshal them into the map
	if len(in.AdditionalFields.Raw) > 0 {
		var additionalFields map[string]interface{}
		if err := json.Unmarshal(in.AdditionalFields.Raw, &additionalFields); err != nil {
			return nil, err
		}
		// Add additional fields to the map, potentially overwriting any duplicates
		for k, v := range additionalFields {
			specMap[k] = v
		}
	}

	// Remove the AdditionalFields key from the map as we don't want it in the final JSON
	delete(specMap, "AdditionalFields")

	// Marshal the combined map back to JSON
	marshal, err := json.Marshal(specMap)

	return marshal, err
}

// MachineStatus defines the observed state of Machine
type MachineStatus struct {
	// Conditions store the status conditions of the Memcached instances
	// Nodes are the names of the machine pods
	Nodes []string `json:"nodes"`
	// +operator-sdk:csv:customresourcedefinitions:type=status
	Conditions []metav1.Condition `json:"conditions,omitempty" patchStrategy:"merge" patchMergeKey:"type" protobuf:"bytes,1,rep,name=conditions"`
}

// Machine is the Schema for the machines API
// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
type Machine struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   MachineSpec   `json:"spec,omitempty"`
	Status MachineStatus `json:"status,omitempty"`
}

//+kubebuilder:object:root=true

// MachineList contains a list of Machine
type MachineList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Machine `json:"items"`
}

func init() {
	SchemeBuilder.Register(&Machine{}, &MachineList{})
}

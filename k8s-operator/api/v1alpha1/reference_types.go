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
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
)

// ReferenceSpec allows any JSON content
// +kubebuilder:validation:Type=object
// +kubebuilder:pruning:PreserveUnknownFields
type ReferenceSpec struct {
	runtime.RawExtension `json:",inline,omitempty"`
}

// ReferenceStatus defines the observed state of Reference
type ReferenceStatus struct {
	// ResourceStatus represents the current status of the reference
	ResourceStatus string `json:"resourceStatus"`
	// Errors contains any errors associated with the reference
	Errors []string `json:"errors,omitempty"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status

// Reference is the Schema for the references API
type Reference struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   ReferenceSpec   `json:"spec,omitempty"`
	Status ReferenceStatus `json:"status,omitempty"`
}

//+kubebuilder:object:root=true

// ReferenceList contains a list of Reference
type ReferenceList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Reference `json:"items"`
}

func init() {
	SchemeBuilder.Register(&Reference{}, &ReferenceList{})
}

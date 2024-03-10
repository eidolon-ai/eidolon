# Azure Authentication Configuration Guide

This guide provides detailed steps on how to configure Azure authentication for your application, including optional Role-Based Access Control (RBAC) settings for enhanced security.

## Step 1: Registering Your Application in Azure

Begin by navigating to the Azure portal and initiating a new "App registration". It's crucial to record the application (client ID) as it will be required in later steps.

## Step 2: Configuring Eidolon for Azure Authentication

To integrate Azure authentication, adjust the `AuthenticationProcessor` setting in your configuration to `AzureJWTProcessor`.

For applications that require Role-Based Access Control (RBAC) to manage functional permissions, the `FunctionalAuthorizer` should be set to `GlobPatternFunctionalAuthorizer`.

### Example Configuration
Below is an illustrative example demonstrating how to configure Eidolon with the `auth.yaml` file:

```yaml
---
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: AuthenticationProcessor
spec:
  implementation: AzureJWTProcessor
  client_id: your_azure_client_id  # Use your Azure app ID here
  tenant_id: your_azure_tenant_id  # Use your Azure tenant ID here
```

## Azure RBAC Configuration

Azure RBAC allows you to manage fine-grained permissions for different entities in your application. Follow these steps if you need to implement RBAC.

### Step 3: Creating Application Roles in Azure (Optional)

Create roles for various permissions by defining them as follows:
- `agents/*/processes/{PERM}`
- Substitute `{PERM}` with specific permissions: `create`, `read`, `update`, `delete`, or `*` to encompass all permissions.

Ensure these roles are assigned to the relevant users or groups. These roles will be reflected in the roles claim of the JWT.

### Step 4: Configuring RBAC in Eidolon

To apply RBAC settings within Eidolon, utilize the following configuration snippet:

```yaml
---
apiVersion: eidolon/v1
kind: Reference
metadata:
  name: FunctionalAuthorizer
spec: GlobPatternFunctionalAuthorizer
```
variable "project_id" {
    type = string
    description = "The id of the GCP project in which you will work"
}

variable "project_number" {
    type = string
    description = "The number of the GCP project in which you will work"
}

variable "region" {
    type = string
    description = "The region where you will deploy your compute engine"
}

variable "zone" {
    type = string
    description = "The zone where you will work on GCP"
}

variable "network" {
    type = string
    description = "The network for the instances"
} 

variable "subnetwork" {
    type = string
    description = "The subnetwork for the instances"
}

variable "service_account_email" {
    type = string
    description = "The email of the service account to attach to the computes engines"
}

variable "user_op_db" {
    type = string
    description = "The user to access to the operational database (Cloud SQL)"
}

variable "password_op_db" {
    type = string
    description = "The password to access to the operational database (Cloud SQL)"
}

variable "roles_permissions" {
    type = list(string)
    description = "The roles to assign to the service account"
    default = [
        "roles/cloudsql.client",
        "roles/storage.objectUser",
        "roles/pubsub.editor"
    ]
}
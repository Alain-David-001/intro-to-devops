output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS service name."
  value       = aws_ecs_service.app.name
}

output "rds_endpoint" {
  description = "RDS MySQL endpoint."
  value       = aws_db_instance.mysql.endpoint
}

output "db_password_secret_arn" {
  description = "Secrets Manager ARN that stores the database password."
  value       = aws_secretsmanager_secret.db_password.arn
}

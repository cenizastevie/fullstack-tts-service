resource "aws_ecs_cluster" "main" {
  name = "${var.bucket_name_prefix}-${var.environment}-cluster"
}

resource "aws_ecs_task_definition" "fastapi" {
  family                   = "${var.bucket_name_prefix}-${var.environment}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  container_definitions    = jsonencode([
    {
      name      = "${var.bucket_name_prefix}-${var.environment}-container"
      image     = "${aws_ecr_repository.fastapi.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "fastapi" {
  name            = "${var.bucket_name_prefix}-${var.environment}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.fastapi.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets         = [aws_subnet.main_a.id, aws_subnet.main_b.id]  # Reference two subnets
    security_groups = [aws_security_group.ecs.id]
  }
}
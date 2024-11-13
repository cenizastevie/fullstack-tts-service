resource "aws_apigatewayv2_api" "fastapi" {
  name          = "${var.bucket_name_prefix}-${var.environment}-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "fastapi" {
  api_id           = aws_apigatewayv2_api.fastapi.id
  integration_type = "HTTP_PROXY"
  integration_uri  = aws_lb_listener.app.arn
}

resource "aws_apigatewayv2_route" "fastapi" {
  api_id    = aws_apigatewayv2_api.fastapi.id
  route_key = "ANY /{proxy+}"
  target    = aws_apigatewayv2_integration.fastapi.id
}

resource "aws_apigatewayv2_stage" "fastapi" {
  api_id      = aws_apigatewayv2_api.fastapi.id
  name        = "$default"
  auto_deploy = true
}
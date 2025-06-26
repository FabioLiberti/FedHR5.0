# FedHR5.0 API Reference

> Complete API documentation for FedHR5.0 federated learning framework

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Core APIs](#core-apis)
   - [Server API](#server-api)
   - [Client API](#client-api)
   - [Privacy API](#privacy-api)
4. [Module APIs](#module-apis)
   - [Well-being Module](#well-being-module)
   - [Skills Module](#skills-module)
   - [Recruitment Module](#recruitment-module)
   - [Benchmarking Module](#benchmarking-module)
   - [Learning Module](#learning-module)
5. [WebSocket API](#websocket-api)
6. [gRPC API](#grpc-api)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Examples](#examples)

## Overview

### Base URLs

```
Production: https://api.fedhr5.yourdomain.com/v1
Staging:    https://staging-api.fedhr5.yourdomain.com/v1
Development: http://localhost:8080/api/v1
```

### API Versioning

The API uses URL versioning. Current version: `v1`

### Content Types

- Request: `application/json`
- Response: `application/json`
- File uploads: `multipart/form-data`

### Common Headers

```http
Content-Type: application/json
Authorization: Bearer <token>
X-Client-ID: <organization-id>
X-Request-ID: <unique-request-id>
```

## Authentication

### OAuth 2.0 Flow

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET&
scope=fedhr5.read fedhr5.write
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "fedhr5.read fedhr5.write"
}
```

### API Key Authentication

```http
GET /api/v1/status
X-API-Key: your-api-key-here
```

## Core APIs

### Server API

#### Initialize Training Round

```http
POST /api/v1/training/rounds
Authorization: Bearer <token>

{
  "round_id": "round_2024_12_001",
  "min_clients": 3,
  "timeout": 3600,
  "aggregation_method": "fedavg",
  "privacy_budget": 0.01
}
```

**Response:**
```json
{
  "round_id": "round_2024_12_001",
  "status": "initialized",
  "created_at": "2024-12-15T10:00:00Z",
  "participants": [],
  "config": {
    "min_clients": 3,
    "timeout": 3600,
    "aggregation_method": "fedavg",
    "privacy_budget": 0.01
  }
}
```

#### Get Round Status

```http
GET /api/v1/training/rounds/{round_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "round_id": "round_2024_12_001",
  "status": "in_progress",
  "participants": [
    {
      "client_id": "org_001",
      "status": "training",
      "progress": 0.75
    },
    {
      "client_id": "org_002",
      "status": "completed",
      "progress": 1.0
    }
  ],
  "privacy_spent": 0.008,
  "metrics": {
    "avg_loss": 0.234,
    "avg_accuracy": 0.912
  }
}
```

#### Aggregate Models

```http
POST /api/v1/training/rounds/{round_id}/aggregate
Authorization: Bearer <token>

{
  "aggregation_method": "fedavg",
  "weights": {
    "org_001": 0.4,
    "org_002": 0.6
  },
  "apply_differential_privacy": true
}
```

**Response:**
```json
{
  "round_id": "round_2024_12_001",
  "aggregation_status": "completed",
  "global_model_id": "model_v1_001",
  "privacy_spent": 0.01,
  "fairness_metrics": {
    "demographic_parity": 0.95,
    "equalized_odds": 0.93
  }
}
```

### Client API

#### Register Client

```http
POST /api/v1/clients/register
Content-Type: application/json

{
  "organization_name": "Manufacturing Corp",
  "organization_id": "org_003",
  "num_employees": 500,
  "data_characteristics": {
    "features": 128,
    "samples": 10000,
    "update_frequency": "daily"
  },
  "capabilities": ["wellbeing", "skills", "recruitment"]
}
```

**Response:**
```json
{
  "client_id": "client_abc123",
  "api_key": "sk_live_abc123...",
  "endpoints": {
    "training": "https://api.fedhr5.com/v1/training",
    "grpc": "grpc://api.fedhr5.com:50051"
  },
  "config": {
    "max_rounds_per_day": 10,
    "privacy_budget_total": 1.0
  }
}
```

#### Submit Model Update

```http
POST /api/v1/clients/{client_id}/updates
Authorization: Bearer <token>
Content-Type: multipart/form-data

round_id=round_2024_12_001
model_update=@model_update.bin
metrics={"loss": 0.23, "accuracy": 0.91}
privacy_spent=0.008
num_samples=1000
```

**Response:**
```json
{
  "update_id": "update_xyz789",
  "status": "accepted",
  "round_id": "round_2024_12_001",
  "timestamp": "2024-12-15T10:30:00Z",
  "validation": {
    "privacy_check": "passed",
    "integrity_check": "passed",
    "size_check": "passed"
  }
}
```

### Privacy API

#### Get Privacy Budget

```http
GET /api/v1/privacy/budget
Authorization: Bearer <token>
X-Client-ID: org_001
```

**Response:**
```json
{
  "client_id": "org_001",
  "total_budget": 1.0,
  "spent_budget": 0.23,
  "remaining_budget": 0.77,
  "breakdown": {
    "wellbeing": 0.10,
    "skills": 0.08,
    "recruitment": 0.05
  },
  "reset_date": "2025-01-01T00:00:00Z"
}
```

#### Request Privacy Allocation

```http
POST /api/v1/privacy/allocate
Authorization: Bearer <token>

{
  "client_id": "org_001",
  "module": "wellbeing",
  "requested_epsilon": 0.02,
  "operation": "model_training",
  "justification": "Monthly well-being analysis"
}
```

**Response:**
```json
{
  "allocation_id": "alloc_123",
  "approved": true,
  "allocated_epsilon": 0.02,
  "expires_at": "2024-12-15T23:59:59Z",
  "conditions": {
    "max_queries": 100,
    "noise_multiplier": 1.1
  }
}
```

## Module APIs

### Well-being Module

#### Submit Well-being Data

```http
POST /api/v1/modules/wellbeing/data
Authorization: Bearer <token>

{
  "timestamp": "2024-12-15T10:00:00Z",
  "data_type": "multimodal",
  "encrypted_payload": "base64_encrypted_data...",
  "metadata": {
    "num_employees": 150,
    "data_points": 4500,
    "modalities": ["survey", "iot", "environmental"]
  }
}
```

**Response:**
```json
{
  "data_id": "wb_data_456",
  "status": "received",
  "processing_status": "queued",
  "privacy_budget_required": 0.01
}
```

#### Get Well-being Insights

```http
GET /api/v1/modules/wellbeing/insights?
  start_date=2024-12-01&
  end_date=2024-12-15&
  aggregation_level=department
Authorization: Bearer <token>
```

**Response:**
```json
{
  "insights": {
    "overall_wellbeing_score": 7.8,
    "trend": "improving",
    "risk_areas": [
      {
        "area": "work_life_balance",
        "score": 6.2,
        "priority": "high"
      }
    ],
    "recommendations": [
      {
        "action": "flexible_hours",
        "impact": "high",
        "implementation_time": "2 weeks"
      }
    ]
  },
  "privacy_guarantee": "ε-differential privacy with ε=0.1",
  "confidence_interval": [7.6, 8.0]
}
```

### Skills Module

#### Create Skills Mapping

```http
POST /api/v1/modules/skills/mapping
Authorization: Bearer <token>

{
  "organization_id": "org_001",
  "taxonomy_version": "v2.1",
  "skills_data": {
    "format": "encrypted_embeddings",
    "data": "base64_encoded_data..."
  }
}
```

**Response:**
```json
{
  "mapping_id": "map_789",
  "status": "processing",
  "estimated_completion": "2024-12-15T11:00:00Z",
  "preview": {
    "total_skills": 1248,
    "unique_roles": 67,
    "coverage": 0.92
  }
}
```

#### Perform Gap Analysis

```http
POST /api/v1/modules/skills/gap-analysis
Authorization: Bearer <token>

{
  "current_skills": ["skill_id_1", "skill_id_2"],
  "target_role": "role_id_123",
  "include_recommendations": true,
  "privacy_level": "high"
}
```

**Response:**
```json
{
  "analysis_id": "gap_analysis_101",
  "gaps": [
    {
      "skill": "Advanced Data Analysis",
      "current_level": 2,
      "required_level": 4,
      "priority": "high"
    }
  ],
  "recommendations": [
    {
      "learning_path_id": "path_456",
      "duration": "3 months",
      "cost": 500,
      "roi_estimate": 2.5
    }
  ],
  "cross_org_percentile": 75
}
```

### Recruitment Module

#### Submit Recruitment Model

```http
POST /api/v1/modules/recruitment/models
Authorization: Bearer <token>

{
  "model_type": "candidate_matching",
  "fairness_constraints": {
    "demographic_parity": 0.05,
    "equalized_odds": 0.05
  },
  "protected_attributes": ["gender", "age_group", "ethnicity"],
  "model_data": "base64_encoded_model..."
}
```

**Response:**
```json
{
  "model_id": "recruit_model_123",
  "validation_status": "passed",
  "fairness_metrics": {
    "demographic_parity_difference": 0.03,
    "equalized_odds_difference": 0.04,
    "disparate_impact": 0.85
  },
  "certification": {
    "compliant": true,
    "certificate_id": "cert_abc123"
  }
}
```

### Benchmarking Module

#### Submit Benchmarking Metrics

```http
POST /api/v1/modules/benchmarking/submit
Authorization: Bearer <token>

{
  "metric_type": "employee_retention",
  "period": "2024-Q4",
  "encrypted_values": {
    "retention_rate": "encrypted_0.88",
    "voluntary_turnover": "encrypted_0.05"
  },
  "computation_proof": "zk_proof_data..."
}
```

**Response:**
```json
{
  "submission_id": "bench_submit_789",
  "status": "validated",
  "blockchain_tx": "0x123abc...",
  "aggregation_round": "2024_Q4_001"
}
```

#### Get Benchmark Results

```http
GET /api/v1/modules/benchmarking/results?
  metric=employee_retention&
  period=2024-Q4&
  comparison_group=industry
Authorization: Bearer <token>
```

**Response:**
```json
{
  "benchmark_results": {
    "your_rank": 3,
    "total_participants": 15,
    "percentile": 80,
    "industry_average": 0.82,
    "top_quartile": 0.89,
    "your_value": 0.88
  },
  "insights": [
    "Your retention rate is 6% above industry average",
    "Top performers focus on career development programs"
  ],
  "privacy_preserved": true,
  "minimum_k_anonymity": 5
}
```

### Learning Module

#### Get Personalized Learning Path

```http
POST /api/v1/modules/learning/recommend
Authorization: Bearer <token>

{
  "employee_profile": {
    "current_skills": ["skill_1", "skill_2"],
    "learning_style": "visual",
    "available_time": "5_hours_per_week"
  },
  "goals": ["promotion", "skill_upgrade"],
  "budget": 1000,
  "use_federated_recommendations": true
}
```

**Response:**
```json
{
  "recommendation_id": "rec_123",
  "learning_paths": [
    {
      "path_id": "path_789",
      "name": "Data Science Fundamentals",
      "duration": "3 months",
      "cost": 499,
      "modules": [
        {
          "module_id": "mod_1",
          "title": "Python for Data Analysis",
          "duration": "2 weeks",
          "format": "interactive_video"
        }
      ],
      "success_rate": 0.78,
      "career_impact": "high"
    }
  ],
  "personalization_score": 0.92,
  "cross_org_validation": true
}
```

## WebSocket API

### Real-time Training Updates

```javascript
// Connection
const ws = new WebSocket('wss://api.fedhr5.com/v1/ws');

// Authentication
ws.send(JSON.stringify({
  type: 'auth',
  token: 'Bearer <token>'
}));

// Subscribe to round updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'round_updates',
  round_id: 'round_2024_12_001'
}));

// Receive updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
};
```

**Message Types:**

```json
// Progress Update
{
  "type": "progress",
  "round_id": "round_2024_12_001",
  "client_id": "org_001",
  "progress": 0.45,
  "eta": "2024-12-15T11:30:00Z"
}

// Aggregation Complete
{
  "type": "aggregation_complete",
  "round_id": "round_2024_12_001",
  "global_model_id": "model_123",
  "improvements": {
    "accuracy": "+2.3%",
    "loss": "-0.05"
  }
}
```

## gRPC API

### Protocol Buffer Definitions

```protobuf
syntax = "proto3";

package fedhr5.v1;

service FederatedLearning {
  rpc RegisterClient(ClientRegistration) returns (ClientConfig);
  rpc SubmitUpdate(ModelUpdate) returns (UpdateResponse);
  rpc GetGlobalModel(ModelRequest) returns (stream ModelChunk);
  rpc StreamMetrics(MetricStream) returns (stream MetricAck);
}

message ClientRegistration {
  string organization_id = 1;
  string organization_name = 2;
  int32 num_employees = 3;
  repeated string capabilities = 4;
}

message ModelUpdate {
  string round_id = 1;
  bytes encrypted_gradients = 2;
  float privacy_spent = 3;
  map<string, float> metrics = 4;
  int32 num_samples = 5;
}
```

### gRPC Client Example (Python)

```python
import grpc
from fedhr5.proto import federated_learning_pb2 as fl_pb2
from fedhr5.proto import federated_learning_pb2_grpc as fl_grpc

# Create channel with credentials
credentials = grpc.ssl_channel_credentials()
channel = grpc.secure_channel('api.fedhr5.com:50051', credentials)

# Create stub
stub = fl_grpc.FederatedLearningStub(channel)

# Register client
registration = fl_pb2.ClientRegistration(
    organization_id="org_001",
    organization_name="Manufacturing Corp",
    num_employees=500,
    capabilities=["wellbeing", "skills"]
)

response = stub.RegisterClient(registration)
print(f"Client ID: {response.client_id}")
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "PRIVACY_BUDGET_EXCEEDED",
    "message": "Privacy budget exceeded for this period",
    "details": {
      "current_budget": 1.0,
      "requested": 0.1,
      "available": 0.0
    },
    "request_id": "req_123abc",
    "timestamp": "2024-12-15T10:00:00Z"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `PRIVACY_BUDGET_EXCEEDED` | 429 | Privacy budget exhausted |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

### Error Handling Best Practices

```python
import requests
from time import sleep

def make_api_request_with_retry(url, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                retry_after = int(e.response.headers.get('Retry-After', 60))
                sleep(retry_after)
            elif e.response.status_code >= 500:  # Server error
                sleep(2 ** attempt)  # Exponential backoff
            else:
                raise  # Don't retry client errors
    raise Exception("Max retries exceeded")
```

## Rate Limiting

### Rate Limit Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1702641600
X-RateLimit-Reset-After: 3600
```

### Rate Limits by Endpoint

| Endpoint Pattern | Limit | Window |
|-----------------|-------|--------|
| `/api/v1/auth/*` | 10 | 1 minute |
| `/api/v1/training/*` | 100 | 1 hour |
| `/api/v1/privacy/*` | 50 | 1 hour |
| `/api/v1/modules/*` | 200 | 1 hour |
| `/api/v1/ws` | 10 connections | Per client |

## Examples

### Complete Training Round Example

```python
import requests
import json
from base64 import b64encode

# Configuration
API_BASE = "https://api.fedhr5.com/v1"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1. Initialize round
round_data = {
    "round_id": f"round_{datetime.now().strftime('%Y%m%d_%H%M')}",
    "min_clients": 3,
    "timeout": 3600,
    "privacy_budget": 0.01
}

response = requests.post(
    f"{API_BASE}/training/rounds",
    headers=headers,
    json=round_data
)
round_info = response.json()
print(f"Round created: {round_info['round_id']}")

# 2. Submit local update
with open("model_update.bin", "rb") as f:
    model_data = b64encode(f.read()).decode()

update_data = {
    "round_id": round_info['round_id'],
    "model_update": model_data,
    "metrics": {
        "loss": 0.234,
        "accuracy": 0.912
    },
    "privacy_spent": 0.008,
    "num_samples": 1000
}

response = requests.post(
    f"{API_BASE}/clients/{CLIENT_ID}/updates",
    headers=headers,
    json=update_data
)
print(f"Update submitted: {response.json()['update_id']}")

# 3. Wait for aggregation
import time
while True:
    response = requests.get(
        f"{API_BASE}/training/rounds/{round_info['round_id']}",
        headers=headers
    )
    status = response.json()['status']
    
    if status == 'completed':
        print("Round completed!")
        break
    elif status == 'failed':
        print("Round failed!")
        break
    
    time.sleep(10)

# 4. Get global model
response = requests.get(
    f"{API_BASE}/models/{round_info['global_model_id']}",
    headers=headers
)
model = response.json()
print(f"Global model accuracy: {model['metrics']['accuracy']}")
```

### Privacy-Preserving Benchmark Example

```python
from fedhr5 import BenchmarkingClient
import numpy as np

# Initialize client
client = BenchmarkingClient(api_key="your-api-key")

# Prepare metrics with differential privacy
retention_rate = 0.88
noisy_retention = retention_rate + np.random.laplace(0, 0.01)  # Add noise

# Submit to benchmark
result = client.submit_metric(
    metric_type="employee_retention",
    value=noisy_retention,
    period="2024-Q4",
    privacy_guarantee="laplace_mechanism",
    epsilon=0.1
)

# Get benchmark results
comparison = client.get_comparison(
    metric="employee_retention",
    period="2024-Q4"
)

print(f"Your rank: {comparison['your_rank']} out of {comparison['total_participants']}")
print(f"Industry average: {comparison['industry_average']}")
```

---

*For more examples and SDKs, visit our [GitHub repository](https://github.com/yourusername/FedHR5.0)*

*API Version: 1.0.0 | Last Updated: December 2024*
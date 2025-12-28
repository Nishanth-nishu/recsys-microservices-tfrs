Project: Microservices-based Recommendation System
Component: Feature Service
Status: Design Finalized
Audience: ML Engineers, Backend Engineers, Future Contributors

1. Purpose of the Feature Service

The Feature Service is responsible for:

Owning online features required by recommendation models

Acting as the single source of truth for user and item features

Decoupling feature computation from model inference

Providing low-latency feature access during inference

This service is model-agnostic and does not perform training or prediction.

2. Data Source

All features are derived from a single interaction log:

feedback-training-service/data/processed/interactions.csv

Interaction Schema
Column	Description
user_id	Unique user identifier
item_id	Unique item identifier
timestamp	Unix timestamp of interaction
label	Implicit positive feedback (1)

Only positive implicit interactions are present.

3. Design Principles

Feature design follows these principles:

Inference Availability
All features must be available at inference time.

Low Latency
Features must be cheap to retrieve and compute.

Model Independence
Features should not depend on a specific model architecture.

Extensibility
Schema must allow future features without breaking consumers.

Cold-Start Safety
Features must support users/items without embeddings.

4. User Features
Rationale

User features capture:

Activity level

Recency of engagement

Feature freshness

These signals are useful for:

Cold-start handling

Ranking bias

Fallback recommendation logic

User Feature Schema
Field	Type	Description
user_id	TEXT (PK)	User identifier
interaction_count	INT	Total interactions
last_interaction_ts	BIGINT	Most recent interaction
updated_at	TIMESTAMP	Feature update time
SQL Definition
CREATE TABLE user_features (
    user_id TEXT PRIMARY KEY,
    interaction_count INT NOT NULL,
    last_interaction_ts BIGINT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

5. Item Features
Rationale

Item features capture:

Popularity

Recency

Feature freshness

Popularity is a strong baseline in recommendation systems and is essential for:

Cold-start items

Fallback recommendations

Ranking signals

Item Feature Schema
Field	Type	Description
item_id	TEXT (PK)	Item identifier
interaction_count	INT	Total interactions
last_interaction_ts	BIGINT	Most recent interaction
updated_at	TIMESTAMP	Feature update time
SQL Definition
CREATE TABLE item_features (
    item_id TEXT PRIMARY KEY,
    interaction_count INT NOT NULL,
    last_interaction_ts BIGINT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

6. Storage Strategy
PostgreSQL (Source of Truth)

Stores all user and item features

Ensures durability and consistency

Allows schema evolution

Redis (Cache Layer – Future Step)

Stores hot features

Used for low-latency inference

Can be rebuilt from PostgreSQL

PostgreSQL is authoritative; Redis is optional and replaceable.\
\
7. What Is Explicitly Out of Scope

The Feature Service does not handle:

Model training

Embedding computation

FAISS indexing

Ranking logic

Business rules

These responsibilities belong to other services.

8. Extension Strategy

Future features may include:

Category-based item features

Temporal decay features

Aggregated session features

All extensions must:

Be backward compatible

Preserve primary keys

Be additive, not destructive

9. Summary

This design defines a stable, minimal, and production-ready contract for feature storage and serving.

Once implemented:

Models can evolve independently

Features can be recomputed safely

Microservices can integrate without tight coupling

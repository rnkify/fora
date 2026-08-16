# Fora Architecture Principles

## 1. Stable core, flexible business layer

Frequently changing commercial values must remain outside core logic.

Examples:

- branding
- pricing
- services
- navigation
- marketing copy
- CTAs
- FAQs
- feature availability
- design tokens

## 2. Stable internal IDs

Business entities use stable machine identifiers independently from
editable marketing labels.

Examples:

- ai_systems
- conversion_copy
- starter
- growth
- scale

## 3. Historical snapshots

Projects preserve commercial values as they existed when the project
was created.

Changing current prices or public labels must not rewrite project
history.

## 4. Provider boundaries

External services must sit behind internal interfaces.

Examples:

- billing
- analytics
- email
- storage
- AI providers

## 5. Production simplicity

Fora V1 is a modular Django monolith.

Do not introduce microservices, a separate SPA frontend, or distributed
infrastructure without a demonstrated operational need.

## 6. Feature boundary

A V1 feature must materially help Fora:

- sell
- deliver
- retain
- operate

Interesting but unnecessary functionality is deferred.

## 7. Configuration migration path

V1 configuration is static and validated.

Future architecture may move frequently edited configuration into:

admin
→ database
→ repository/service
→ application

Views and templates should not need to know where configuration is
stored.

# FROM node:22-alpine

# RUN corepack enable && corepack prepare pnpm@latest --activate

# WORKDIR /app

# COPY package.json pnpm-lock.yaml ./

# RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store \
#     pnpm install --frozen-lockfile --node-linker=hoisted

# COPY . .

# ENV CI=true

# CMD ["pnpm", "dev", "--host"]

# syntax=docker/dockerfile:1

# ─── Stage 1: base ───────────────────────────────────────────────
FROM node:22-slim AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app


# ─── Stage 2: dependencies (только prod для финального образа) ───
FROM base AS deps

COPY package.json pnpm-lock.yaml ./
# Кэшируем store — сильно ускоряет повторные сборки
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --prod --frozen-lockfile


# ─── Stage 3: build ──────────────────────────────────────────────
FROM base AS build

# Копируем зависимости из предыдущего stage + dev-зависимости
# COPY --from=deps /pnpm /pnpm
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile

COPY . .
# Если нужно передать переменные окружения на этапе сборки
# ARG VITE_BACKEND_URL
# ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
RUN pnpm run build-only


# ─── Stage 4: production (nginx) ─────────────────────────────────
FROM nginx:alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Права на всякий случай
RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
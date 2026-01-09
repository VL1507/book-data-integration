FROM node:22-alpine

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

ENV CI=true

COPY . .

RUN pnpm install --frozen-lockfile


CMD ["pnpm", "dev", "--host"]
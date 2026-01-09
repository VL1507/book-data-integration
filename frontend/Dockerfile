FROM node:22-alpine

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Копируем только манифесты для кэширования
COPY package.json pnpm-lock.yaml ./

# Устанавливаем с hoisted структурой — решает проблему с Vite
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile --node-linker=hoisted

# Теперь копируем весь код
COPY . .

ENV CI=true

CMD ["pnpm", "dev", "--host"]
FROM node:18-bullseye-slim AS base
RUN npm install -g pnpm
RUN npm install -g turbo

# Build pruned project target; this includes /json that is only remote dependencies, and /full that includes our code
FROM base AS builder
WORKDIR /app
COPY . .
RUN turbo prune eidolon-ui2 --docker

# Install remote dependencies first, then copy over project
FROM base AS base_installer
WORKDIR /app
COPY .gitignore .gitignore
COPY --from=builder /app/out/json/ .
RUN pnpm install

# Build eidolon-components first
FROM base_installer as eidolon_components_builder
WORKDIR /app/packages/eidolon-components
RUN pnpm run build

# Build from our project, which will be constant cache misses
FROM base_installer as installer
COPY --from=builder /app/out/full/ .
COPY --from=eidolon_components_builder /app/packages/eidolon-components/dist /app/packages/eidolon-components/dist
COPY .eslintrc.js .eslintrc.js
RUN pnpm --prefix apps/eidolon-ui2 run build

# Build the actual image to run
FROM base AS runner
WORKDIR /app

# Don't run production as root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

COPY --from=installer /app/apps/eidolon-ui2/next.config.js .
COPY --from=installer /app/apps/eidolon-ui2/package.json .
# Leverage standalone output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=installer --chown=nextjs:nodejs /app/apps/eidolon-ui2/.next/standalone ./
COPY --from=installer --chown=nextjs:nodejs /app/apps/eidolon-ui2/.next/static ./apps/eidolon-ui2/.next/static
COPY --from=installer --chown=nextjs:nodejs /app/apps/eidolon-ui2/public ./apps/eidolon-ui2/public
# Throw default envars in the image so that we can run locally with less overrides
ENV NEXTAUTH_URL=http://localhost:3000/api/auth
ENV AUTH_TRUST_HOST=http://localhost:3000
ENV NEXTAUTH_SECRET=secret
ENV EIDOLON_AUTH_PROVIDERS=""
CMD node apps/eidolon-ui2/server.js
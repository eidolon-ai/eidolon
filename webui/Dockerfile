FROM node:18-bullseye-slim
COPY . .
RUN npm install -g pnpm
RUN pnpm install turbo -w
RUN pnpm install
RUN pnpm run build
CMD ["pnpm", "run", "start"]
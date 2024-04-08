FROM node:20.4.0 AS builder
WORKDIR /temp

RUN npm config set strict-ssl false
RUN npm config set registry http://registry.npmjs.org/

COPY . .

RUN npm install
RUN npm run build


FROM node:20.4.0 AS server
WORKDIR /app

COPY --from=builder /temp/next.config.mjs ./next.config.mjs
COPY --from=builder /temp/public ./public
COPY --from=builder /temp/.next ./.next
COPY --from=builder /temp/node_modules ./node_modules
COPY --from=builder /temp/package.json ./package.json

CMD [ "npm", "run", "start" ]
FROM node:latest

WORKDIR /opt/app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "build"]

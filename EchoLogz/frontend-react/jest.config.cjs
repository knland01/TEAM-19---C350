module.exports = {
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest",
  },
  moduleFileExtensions: ["js", "jsx", "json", "node"],
  roots: ["<rootDir>/../tests"],
  moduleDirectories: ["node_modules", "frontend-react/node_modules"],
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"]
};

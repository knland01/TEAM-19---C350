/*
MODULE: eslint.config.js 
ESLint = code-quality checker for JavaScript and React. 
ESLint scans all Javascipt and JSX files inside frontend-react (unless folder is explicitly ignored) - 
Eslint looks for:
----- Anything that violates rules defined in this module: 
        --> ex: bugs, bad patterns, inconsistent style, unused variables, incorrect React Hook useage, missing imports, typos that break builds.
*/

import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    rules: {
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
    },
  },
])

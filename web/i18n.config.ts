import { readFile } from 'fs/promises';
import { resolve } from 'path';
import type { I18nConfig } from 'next-i18next/proxy';

const i18nConfig: I18nConfig = {
  defaultNS: 'common',
  fallbackLng: 'en',
  localeInPath: false,
  ns: ['auth', 'builds', 'common'],
  resourceLoader: async (language: string, namespace: string) => {
    let content: string;

    if (process.env.NODE_ENV === 'development') {
      content = await readFile(resolve(process.cwd(), `web/i18n/locales/${language}/${namespace}.json`), 'utf-8');

      return JSON.parse(content);
    }

    return import(`./i18n/locales/${language}/${namespace}.json`);
  },
  supportedLngs: ['en'],
};

export default i18nConfig;

import { createProxy } from 'next-i18next/proxy';

// configs
import i18nConfig from './i18n.config';

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|assets|favicon.ico|sw.js|site.webmanifest).*)'],
};
export const proxy = createProxy(i18nConfig);

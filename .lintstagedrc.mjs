function quote(filename) {
  return `"${filename}"`;
}

export default {
  // format javascript related files
  '**/*.{cjs,js,json,mjs,ts,tsx}': (filenames) => [`prettier --write ${filenames.map(quote).join(' ')}`],
  // format python files
  '**/*.py': (filenames) => [
    `.venv/bin/isort ${filenames.map(quote).join(' ')}`,
    `.venv/bin/black ${filenames.map(quote).join(' ')}`,
  ],
};

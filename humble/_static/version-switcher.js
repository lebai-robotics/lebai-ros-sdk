(async function createVersionSwitcher() {
  const mount = document.createElement('div');
  mount.style.margin = '1rem 0';

  const label = document.createElement('label');
  label.textContent = 'Docs version: ';
  label.setAttribute('for', 'docs-version-select');

  const select = document.createElement('select');
  select.id = 'docs-version-select';

  const siteBase = new URL('../../', document.currentScript.src);
  const versionsUrl = new URL('versions.json', siteBase);
  const response = await fetch(versionsUrl);
  const versions = await response.json();
  const current = location.pathname
    .replace(siteBase.pathname, '')
    .split('/')
    .filter(Boolean)[0];

  for (const version of versions) {
    const option = document.createElement('option');
    option.textContent = version.label;
    option.value = new URL(`${version.path}/`, siteBase).toString();
    option.selected = version.path === current;
    select.appendChild(option);
  }

  select.addEventListener('change', () => {
    location.href = select.value;
  });

  mount.appendChild(label);
  mount.appendChild(select);

  const main = document.querySelector('div.body') || document.body;
  main.prepend(mount);
}());

(function initializeVersionSwitcher() {
  const scriptUrl = document.currentScript.src;

  async function createVersionSwitcher() {
    const mount = document.createElement('div');
    mount.id = 'docs-version-switcher';
    mount.style.margin = '1rem 0';

    const label = document.createElement('label');
    label.textContent = 'Docs version: ';
    label.setAttribute('for', 'docs-version-select');

    const select = document.createElement('select');
    select.id = 'docs-version-select';

    const siteBase = new URL('../../', scriptUrl);
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

    const content = document.querySelector('.wy-nav-content') || document.body;
    content.prepend(mount);
  }

  function start() {
    createVersionSwitcher().catch((error) => {
      console.error('Unable to load documentation versions', error);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
}());

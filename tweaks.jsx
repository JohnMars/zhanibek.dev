/* Tweaks panel — wired to site-wide settings. */
const { useState, useEffect } = React;

function ZMPanel() {
  const [theme,    setTheme]    = useState(() => window.ZM?.getTheme()     || "system");
  const [density,  setDensity]  = useState(() => window.ZM?.getDensity()   || "comfy");
  const [list,     setList]     = useState(() => window.ZM?.getListStyle() || "list");
  const [showRT,   setShowRT]   = useState(() => window.ZM?.getReadtime() ?? true);

  useEffect(() => { window.ZM?.setTheme(theme);    }, [theme]);
  useEffect(() => { window.ZM?.setDensity(density);}, [density]);
  useEffect(() => { window.ZM?.setListStyle(list); }, [list]);
  useEffect(() => { window.ZM?.setReadtime(showRT);}, [showRT]);

  return (
    <TweaksPanel title="Tweaks">
      <TweakSection title="Appearance">
        <TweakRadio
          label="Theme"
          value={theme}
          onChange={setTheme}
          options={[
            { label: "Light",  value: "light"  },
            { label: "Dark",   value: "dark"   },
            { label: "System", value: "system" }
          ]}
        />
        <TweakRadio
          label="Density"
          value={density}
          onChange={setDensity}
          options={[
            { label: "Compact", value: "compact" },
            { label: "Comfy",   value: "comfy"   },
            { label: "Airy",    value: "airy"    }
          ]}
        />
      </TweakSection>

      <TweakSection title="Article list">
        <TweakRadio
          label="Style"
          value={list}
          onChange={setList}
          options={[
            { label: "List",  value: "list"  },
            { label: "Cards", value: "cards" },
            { label: "Table", value: "table" }
          ]}
        />
        <TweakToggle
          label="Show reading time"
          value={showRT}
          onChange={setShowRT}
        />
      </TweakSection>
    </TweaksPanel>
  );
}

const root = document.getElementById("tweaks-root");
if (root) ReactDOM.createRoot(root).render(<ZMPanel />);

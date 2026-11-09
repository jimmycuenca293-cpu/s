# -*- coding: utf-8 -*-
import re
WA_PATH=re.search(r'WA_PATH="([^"]+)"',open('/tmp/claude-0/-home-user-s/7394aa38-735a-5cd1-af51-c01a7780d2eb/scratchpad/tg/brand.py',encoding='utf-8').read()).group(1)
WA_SVG=f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="{WA_PATH}"/></svg>'
def _i(body): return f'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
ICON={
'fridge':_i('<rect x="13" y="5" width="22" height="38" rx="3"/><path d="M13 20h22"/><path d="M18 11v5M18 25v8"/>'),
'freezer':_i('<rect x="5" y="16" width="38" height="22" rx="3"/><path d="M5 22h38"/><path d="M20 28h8"/><path d="M12 38v3M36 38v3"/>'),
'washer':_i('<rect x="9" y="5" width="30" height="38" rx="3"/><path d="M9 14h30"/><circle cx="24" cy="29" r="9"/><path d="M19 29c2-3 3 3 5 0s3 3 5 0"/><circle cx="15" cy="9.5" r="1"/>'),
'dryer':_i('<rect x="9" y="5" width="30" height="38" rx="3"/><path d="M9 14h30"/><circle cx="24" cy="29" r="9"/><circle cx="24" cy="29" r="4"/><circle cx="15" cy="9.5" r="1"/>'),
'tower':_i('<rect x="11" y="3" width="26" height="42" rx="3"/><path d="M11 24h26"/><circle cx="24" cy="14" r="5"/><circle cx="24" cy="35" r="6"/>'),
'stove':_i('<rect x="7" y="6" width="34" height="37" rx="3"/><path d="M7 17h34"/><circle cx="16" cy="11.5" r="2"/><circle cx="32" cy="11.5" r="2"/><rect x="12" y="23" width="24" height="14" rx="2"/>'),
'oven':_i('<rect x="6" y="9" width="36" height="30" rx="3"/><path d="M6 17h36"/><rect x="11" y="21" width="26" height="14" rx="2"/><circle cx="14" cy="13" r="1.3"/><circle cx="24" cy="13" r="1.3"/><circle cx="34" cy="13" r="1.3"/>'),
'cooktop':_i('<rect x="5" y="14" width="38" height="22" rx="3"/><circle cx="15" cy="21" r="3.5"/><circle cx="33" cy="21" r="3.5"/><circle cx="15" cy="30" r="2.5"/><circle cx="33" cy="30" r="2.5"/>'),
'hood':_i('<path d="M17 5h14l6 16H11z"/><path d="M4 21h40v6H4z"/><path d="M14 33v8M24 33v8M34 33v8"/>'),
'microwave':_i('<rect x="5" y="11" width="38" height="26" rx="3"/><rect x="9" y="15" width="22" height="18" rx="2"/><circle cx="37" cy="19" r="1.5"/><path d="M35 26h4M35 30h4"/>'),
'dishwasher':_i('<rect x="8" y="5" width="32" height="38" rx="3"/><path d="M8 13h32"/><circle cx="14" cy="9" r="1"/><path d="M14 25h20M16 25v8M24 25v8M32 25v8"/>'),
'pin':_i('<path d="M24 44s14-13 14-24a14 14 0 10-28 0c0 11 14 24 14 24z"/><circle cx="24" cy="20" r="5"/>'),
'help':_i('<circle cx="24" cy="24" r="18"/><path d="M18 19a6 6 0 1112 0c0 4-6 4-6 9"/><path d="M24 34v.5"/>'),
'chat':_i('<path d="M8 10h32v22H20l-8 8v-8H8z"/>'),
'wrench':_i('<path d="M30 8a9 9 0 00-8 12L8 34l6 6 14-14a9 9 0 0012-8l-6 5-5-1-1-5z"/>'),
'home':_i('<path d="M6 24L24 8l18 16"/><path d="M12 22v18h24V22"/><path d="M20 40V28h8v12"/>'),
'shield':_i('<path d="M24 6l14 5v11c0 9-6 16-14 20-8-4-14-11-14-20V11z"/><path d="M17 24l5 5 9-10"/>'),
'doc':_i('<path d="M12 5h18l8 8v30H12z"/><path d="M30 5v8h8"/><path d="M17 22h14M17 29h14M17 36h9"/>'),
}
# Marca: puerta de lavadora/horno + llave
LOGO_MARK='''<svg viewBox="0 0 64 56" aria-hidden="true"><defs><linearGradient id="lg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fd3e6"/><stop offset="1" stop-color="#0e93b0"/></linearGradient></defs><rect x="3" y="3" width="42" height="50" rx="9" fill="#fff"/><rect x="3" y="3" width="42" height="14" rx="9" fill="url(#lg1)"/><circle cx="13" cy="10" r="2.2" fill="#fff"/><circle cx="21" cy="10" r="2.2" fill="#fff" opacity=".7"/><circle cx="24" cy="34" r="13" fill="none" stroke="#0c2740" stroke-width="3.6"/><circle cx="24" cy="34" r="7" fill="url(#lg1)" opacity=".85"/><path d="M42 18a9 9 0 0 0-11.6 10.8L19 40.2a3.2 3.2 0 0 0 4.5 4.5l11.4-11.4A9 9 0 0 0 46 22l-5 3.4-4.4-.9-.9-4.4z" fill="#ffc83a" stroke="#0c2740" stroke-width="1.8" stroke-linejoin="round" transform="translate(4 -2)"/></svg>'''

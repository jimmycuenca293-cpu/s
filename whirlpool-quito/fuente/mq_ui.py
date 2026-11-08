# -*- coding: utf-8 -*-
import re
WA_PATH="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"
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

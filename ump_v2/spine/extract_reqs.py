import os
import re

directories = [
    r'C:\Users\vinta\OneDrive - Assistants Company\Apps\VTE\Data Folder',
    r'C:\Users\vinta\OneDrive - Assistants Company\Apps\VTE\Notebook',
    r'C:\Users\vinta\OneDrive - Assistants Company\Apps\New VTE Learn\Txt Files'
]

keywords = ['objective', 'feature', 'function', 'expectation', 'real world use', 'output', 'phase', 'ui', 'homepage', 'dashboard']

output_file = r'c:\Bintloop\VTE\ump_v2\spine\master_audit_plan.md'

with open(output_file, 'w', encoding='utf-8') as out:
    out.write('# VTE Master Audit & Execution Plan\n\n')
    out.write('Extracted from Original Source Notebooks and Text Files.\n\n')
    
    for d in directories:
        if not os.path.exists(d):
            continue
            
        for root, _, files in os.walk(d):
            for file in files:
                if not file.endswith('.txt'):
                    continue
                
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    out.write(f'## Source: {file}\n')
                    
                    found_something = False
                    for i, line in enumerate(lines):
                        line_lower = line.lower()
                        # Very basic heuristic: if it looks like a header or bullet containing a keyword
                        if any(kw in line_lower for kw in keywords) and len(line.strip()) < 150:
                            if ':' in line or line.strip().startswith('-') or line.strip().startswith('#'):
                                out.write(f'- {line.strip()}\n')
                                found_something = True
                                
                    if not found_something:
                        out.write('- (No explicit dense objective headers found, requires deep manual reading if needed.)\n')
                    out.write('\n')
                except Exception as e:
                    out.write(f'- Error reading {file}: {str(e)}\n\n')

print("Extraction complete. Audit plan saved to master_audit_plan.md")

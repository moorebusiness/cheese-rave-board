// Run in the State Election Board results page (results.okelections.gov/OKER/?elecDate=20261103, State Results tab).
// Returns the okrelay.json object: {at, src, races:[{id, rep, cands:[{name, party, votes}]}]}
(() => {
  const t = document.body.innerText;
  const asOf = (t.match(/Current as of ([A-Za-z]{3} \d+, \d{4}, [\d:]+ [AP]M)/) || [])[1];
  const OFF = {'GOVERNOR':'OK-GOV', 'LIEUTENANT GOVERNOR':'OK-LG', 'ATTORNEY GENERAL':'OK-AG', 'STATE TREASURER':'OK-TREAS',
    'SUPERINTENDENT OF PUBLIC INSTRUCTION':'OK-SUPT', 'COMMISSIONER OF LABOR':'OK-LABOR', 'INSURANCE COMMISSIONER':'OK-INS',
    'CORPORATION COMMISSIONER':'OK-CORP', 'UNITED STATES SENATOR':'OK-SEN', 'STATE AUDITOR AND INSPECTOR':'OK-AUD'};
  const idOf = h => {
    let m;
    if ((m = h.match(/^STATE QUESTION NO\. (\d+)/))) return 'SQ' + m[1];
    if (!h.startsWith('FOR ')) return null;
    const o = h.slice(4).trim();
    if (OFF[o]) return OFF[o];
    if ((m = o.match(/^UNITED STATES REPRESENTATIVE DISTRICT 0?(\d+)$/))) return 'OK-0' + m[1];
    if ((m = o.match(/^STATE SENATOR DISTRICT (\d+)$/))) return 'OK-SD' + m[1];
    if ((m = o.match(/^STATE REPRESENTATIVE DISTRICT (\d+)$/))) return 'OK-HD' + m[1];
    return null;
  };
  const races = [];
  for (const b of t.split(/\n(?=(?:FOR [A-Z][^\n]*|STATE QUESTION NO\.[^\n]*)\n[\d,]+ of )/)){   // a heading, then its precinct line
    const id = idOf(b.split('\n')[0].trim()); if (!id) continue;
    const pm = b.match(/([\d,]+) of ([\d,]+)\s\(([\d.]+)%\)/);   // (a no-break space before the percentage)
    const cands = [...b.matchAll(/^(.+?)\t([\d,]+)\t?[ \t]*$/gm)].map(m => {
      let name = m[1].trim(), party = '';
      const pp = name.match(/^(.*) \(([A-Z]{3})\)$/); if (pp){ name = pp[1]; party = pp[2]; }
      if (/- YES$/.test(name)) name = 'Yes'; else if (/- NO$/.test(name)) name = 'No';
      return {name, party, votes: +m[2].replace(/,/g, '')};
    }).filter(c => c.name !== 'Total');
    if (cands.length >= 2) races.push({id, rep: pm ? +pm[3] : 0, cands});
  }
  const at = asOf ? new Date(asOf.replace(',', '').replace(/, (\d+:)/, ' $1') + ' CST') : new Date();
  return {at: (isNaN(at) ? new Date() : at).toISOString(), asOf, src: 'Oklahoma State Election Board, unofficial', races};
})()

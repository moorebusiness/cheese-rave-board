// Cheese Rave push archive
// Saves every photo and clip sent to the board (push.html) into a Google Drive folder, untinted, named by time.
// The booth board downloads each push from the relay and sends the file here as it arrives (Google's servers can't
// reach the relay themselves). Pushes sent before showtime (testing) go in a "Testing" subfolder.
// Deploy: Deploy > New deployment > Web app, Execute as: Me, Who has access: Anyone. The board opens with
// ?archive=<deployment ID>.

const KEY = 'PUSH_CODE_HERE';   // the push code; only the copy in Apps Script holds the real one
const FOLDER = 'Cheese Rave pushes';
const TZ = 'America/Chicago';
const SHOW_START = Date.parse('2026-11-03T18:00:00-06:00');
const MAX_BYTES = 25 * 1024 * 1024;
const EXT = {'image/jpeg':'jpg', 'image/png':'png', 'image/gif':'gif', 'image/webp':'webp', 'image/heic':'heic', 'image/heif':'heif',
  'video/mp4':'mp4', 'video/quicktime':'mov', 'video/webm':'webm', 'video/x-m4v':'m4v'};

// Run this once from the editor (Run > setup) to grant Drive access and create the folder.
function setup(){
  const f = getFolder(false);
  Logger.log('Archive folder: ' + f.getUrl());
}

function doGet(){ return out({ok:true, archive:FOLDER}); }

function doPost(e){
  let p;
  try { p = JSON.parse(e.postData.contents); } catch (err) { return out({ok:false, error:'bad request'}); }
  if (!p || p.key !== KEY) return out({ok:false, error:'wrong key'});
  const id = String(p.id || ''), type = String(p.type || '').toLowerCase();
  if (!/^[A-Za-z0-9]{6,32}$/.test(id)) return out({ok:false, error:'bad id'});
  if (!/^(image|video)\/[a-z0-9.+-]+$/.test(type)) return out({ok:false, error:'not a photo or video'});
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(45000)) return out({ok:false, error:'busy', retry:true});
  try {
    const when = new Date(Math.round((+p.time || Date.now() / 1000) * 1000));
    const folder = getFolder(when.getTime() < SHOW_START);
    if (folder.searchFiles('title contains "' + id + '" and trashed = false').hasNext()) return out({ok:true, dup:true});
    if (!p.data) return out({ok:false, error:'no file'});
    const blob = Utilities.newBlob(Utilities.base64Decode(String(p.data)), type);
    const size = blob.getBytes().length;
    if (!size || size > MAX_BYTES) return out({ok:false, error:'size ' + size});
    const kind = type.indexOf('video/') === 0 ? 'clip' : 'photo';
    blob.setName(Utilities.formatDate(when, TZ, 'yyyy-MM-dd HH.mm.ss') + ' ' + kind + ' ' + id + '.' + (EXT[type] || type.split('/')[1].replace(/[^a-z0-9]/g, '')));
    const f = folder.createFile(blob);
    return out({ok:true, saved:true, name:f.getName()});
  } catch (err) {
    return out({ok:false, error:String(err && err.message || err).slice(0, 200), retry:true});
  } finally { lock.releaseLock(); }
}

function getFolder(testing){
  const props = PropertiesService.getScriptProperties();
  const k = testing ? 'testFolder' : 'folder';
  const known = props.getProperty(k);
  if (known){ try { const f = DriveApp.getFolderById(known); if (!f.isTrashed()) return f; } catch (e) {} }
  let f;
  if (testing){ const root = getFolder(false), it = root.getFoldersByName('Testing'); f = it.hasNext() ? it.next() : root.createFolder('Testing'); }
  else { const it = DriveApp.getRootFolder().getFoldersByName(FOLDER); f = it.hasNext() ? it.next() : DriveApp.createFolder(FOLDER); }
  props.setProperty(k, f.getId());
  return f;
}

function out(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

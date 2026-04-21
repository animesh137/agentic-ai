export const MAX_UPLOAD_BYTES = 25 * 1024 * 1024;

export function validateClientUploadSize(sizeBytes: number): { ok: boolean; message: string } {
  if (sizeBytes <= MAX_UPLOAD_BYTES) return { ok: true, message: '' };
  return { ok: false, message: 'File too large. Max size is 25 MB.' };
}

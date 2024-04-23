export class HttpException extends Error {
  status: number;
  statusText: string;

  constructor(statusText: string, status: number) {
    super(`HTTP Error: ${status} ${statusText}`)
    this.status = status;
    this.statusText = statusText;
  }
}

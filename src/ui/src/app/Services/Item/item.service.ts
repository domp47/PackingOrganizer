import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { BaseService } from '../base.service';

@Injectable({
  providedIn: 'root',
})
export class ItemService extends BaseService {
  constructor(private http: HttpClient, snackBar: MatSnackBar) {
    super('items', snackBar);
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.url}/${id}`).pipe(
      map((data) => data),
      catchError((err) => this.handleError('Error Deleting Item', err))
    );
  }
}

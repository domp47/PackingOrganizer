import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { BaseService } from '../base.service';

@Injectable({
  providedIn: 'root'
})
export class BoxService extends BaseService {
  constructor(private http: HttpClient, snackBar: MatSnackBar) { 
    super("boxes", snackBar);
  }

  list(pageSize: number | null = null, pageNumber: number | null = null, filter: string | null = null): Observable<any>{
    var params = new HttpParams();

    if(pageSize != null)
      params = params.set('page_size', pageSize.toString());
    if(pageNumber != null)
      params = params.set('page_number', pageNumber.toString());
    if(filter != null)
      params = params.set('filter', filter);

    return this.http.get(`${this.url}`, { params: params }).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Getting Boxes", err))
    );
  }

  add(obj: any): Observable<any> {
    return this.http.post(`${this.url}`, obj).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Adding Box", err))
    );
  }

  get(id: number): Observable<any> {
    return this.http.get(`${this.url}/${id}`).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Getting Box", err))
    );
  }

  update(id: number, obj: any): Observable<any> {
    return this.http.put(`${this.url}/${id}`, obj).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Updating Box", err))
    );
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.url}/${id}`).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Deleting Box", err))
    );
  }

  listItems(id: number, pageSize: number | null = null, pageNumber: number | null = null, filter: string | null = null): Observable<any>{
    var params = new HttpParams();

    if(pageSize != null)
      params = params.set('page_size', pageSize.toString());
    if(pageNumber != null)
      params = params.set('page_number', pageNumber.toString());
    if(filter != null)
      params = params.set('filter', filter);

    return this.http.get(`${this.url}/${id}/items`, { params: params }).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Getting Items", err))
    );
  }

  addItem(id: any, obj: any): Observable<any> {
    return this.http.post(`${this.url}/${id}/items`, obj).pipe(
      map(data => data),
      catchError(err => this.handleError("Error Adding Item", err))
    );
  }

  getLabel(id: number): void {
    window.open(`${this.url}/${id}/label`, "_blank");
  }
}

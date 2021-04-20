import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';

export class BaseService {

    protected url: string;

    constructor(route: string, private snackBar: MatSnackBar) { 
        this.url = environment.apiBaseUrl + route;
    }

    handleError(title: string, err: Response | any): Observable<any> {
        this.snackBar.open(`${title}: ${err?.error}`, undefined, { duration: 5000 });
        return of();
    }
}
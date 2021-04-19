import { CollectionViewer } from '@angular/cdk/collections';
import { DataSource } from '@angular/cdk/table';
import { BehaviorSubject, Observable } from 'rxjs';

export class BaseDataSource implements DataSource<Object> {

    protected subject = new BehaviorSubject<Object[]>([]);

    dataCount: number = 0;

    connect(collectionViewer: CollectionViewer): Observable<Object[] | readonly Object[]> {
        return this.subject.asObservable();
    }
    disconnect(collectionViewer: CollectionViewer): void {
        this.subject.complete();
    }

    clearTable(){
        this.subject.next([]);
        this.dataCount = 0;
    }
}
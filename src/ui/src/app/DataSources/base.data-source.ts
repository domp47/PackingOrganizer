import { CollectionViewer } from '@angular/cdk/collections';
import { DataSource } from '@angular/cdk/table';
import { BehaviorSubject, Observable } from 'rxjs';

export class BaseDataSource implements DataSource<any> {
  protected subject = new BehaviorSubject<any[]>([]);

  dataCount = 0;

  connect(
    _collectionViewer: CollectionViewer
  ): Observable<any[] | readonly any[]> {
    return this.subject.asObservable();
  }
  disconnect(_collectionViewer: CollectionViewer): void {
    this.subject.complete();
  }

  clearTable() {
    this.subject.next([]);
    this.dataCount = 0;
  }
}

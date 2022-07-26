import { BoxService } from '../Services/Box/box.service';
import { BaseDataSource } from './base.data-source';

export class ItemDataSource extends BaseDataSource {
  constructor(private boxService: BoxService) {
    super();
  }

  loadItems(
    id: number,
    pageNumber: number,
    pageSize: number,
    filter: string | null = null
  ): void {
    this.boxService
      .listItems(id, pageSize, pageNumber, filter)
      .subscribe((r) => {
        this.dataCount = r.count;
        this.subject.next(r.result);
      });
  }
}

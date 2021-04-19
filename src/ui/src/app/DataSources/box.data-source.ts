import { BoxService } from '../Services/Box/box.service';
import { BaseDataSource } from './base.data-source';

export class BoxDataSource extends BaseDataSource {

    constructor(private boxService: BoxService) {
        super();
    }

    loadBoxes(pageNumber: number, pageSize: number, filter: string | null = null): void{
        this.boxService.list(pageSize, pageNumber, filter).subscribe(r => {
            this.dataCount = r.count;
            this.subject.next(r.result);
        });
    }
}
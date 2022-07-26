import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { BoxDataSource } from 'src/app/DataSources/box.data-source';
import { BoxService } from 'src/app/Services/Box/box.service';

@Component({
  selector: 'app-boxes',
  templateUrl: './boxes.component.html',
  styleUrls: ['./boxes.component.scss'],
})
export class BoxesComponent implements OnInit {
  @ViewChild(MatPaginator, { static: true }) paginator!: MatPaginator;

  displayedColumns: string[] = ['label', 'description', 'qr', 'actions'];
  dataSource!: BoxDataSource;

  lastRowClicked = 0;
  lastRowTime = 0;

  constructor(private boxService: BoxService, private router: Router) {}

  ngOnInit(): void {
    this.dataSource = new BoxDataSource(this.boxService);
  }

  ngAfterViewInit(): void {
    this.paginator.page.pipe(tap(() => this.getBoxes())).subscribe();
    this.getBoxes();
  }

  getBoxes() {
    this.dataSource.loadBoxes(
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }

  rowClicked(row: any) {
    if (
      this.lastRowClicked === row.id &&
      Date.now() - this.lastRowTime <= 500
    ) {
      this.router.navigateByUrl('/box/' + row.id + '/view');
    } else {
      this.lastRowClicked = row.id;
      this.lastRowTime = Date.now();
    }
  }

  getLabel(id: number): void {
    this.boxService.getLabel(id);
  }

  getAllLabels(): void {
    this.boxService.getAllLabels();
  }
}

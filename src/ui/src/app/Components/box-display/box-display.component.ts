import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { BoxDataSource } from 'src/app/DataSources/box.data-source';
import { BoxService } from 'src/app/Services/Box/box.service';

@Component({
  selector: 'app-box-display',
  templateUrl: './box-display.component.html',
  styleUrls: ['./box-display.component.scss']
})
export class BoxDisplayComponent implements OnInit {

  @ViewChild(MatPaginator, { static: true }) paginator!: MatPaginator;

  displayedColumns: string[] = ['label', 'description', 'actions'];
  dataSource!: BoxDataSource;

  lastRowClicked: number = 0;
  lastRowTime: number = 0;

  constructor(private boxService: BoxService, private router: Router) { }

  ngOnInit(): void {
    this.dataSource = new BoxDataSource(this.boxService);
  }

  ngAfterViewInit(): void {
    this.paginator.page
    .pipe(tap(() => this.getBoxes()))
    .subscribe();
    this.getBoxes();
  }

  getBoxes(){
    this.dataSource.loadBoxes(this.paginator.pageIndex, this.paginator.pageSize);
  }

  rowClicked(row: any){
    if(this.lastRowClicked === row.id && Date.now()-this.lastRowTime <= 500){
      // this.router.navigateByUrl("/buildings/"+this.id+"/floors/view/"+row.id);
    }else{
      this.lastRowClicked = row.id;
      this.lastRowTime = Date.now();
    }
  }
}

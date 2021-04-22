import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { ActivatedRoute } from '@angular/router';
import { ItemDataSource } from 'src/app/DataSources/item.data-source';
import { debounceTime, first, tap } from 'rxjs/operators';
import { BoxService } from 'src/app/Services/Box/box.service';
import { BaseViewComponent } from '../base-view.component';
import { FormControl } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';
import { ItemService } from 'src/app/Services/Item/item.service';

@Component({
  selector: 'app-box-view',
  templateUrl: './box-view.component.html',
  styleUrls: ['./box-view.component.scss']
})
export class BoxViewComponent extends BaseViewComponent implements OnInit {
  
  @ViewChild(MatPaginator, { static: true }) paginator!: MatPaginator;

  displayedColumns = ["name", "actions"];
  dataSource!: ItemDataSource;
  
  itemSearchControl: FormControl = new FormControl();
  itemFilter: string | null = null;
  box: any;

  constructor(activatedRoute: ActivatedRoute, private boxService: BoxService, private dialog: MatDialog, private itemService: ItemService) { 
    super(activatedRoute);
  }

  ngOnInit(): void {
    this.dataSource = new ItemDataSource(this.boxService);
    super.ngOnInit();

    this.itemSearchControl.valueChanges.pipe(debounceTime(750)).subscribe(value => {
      this.itemFilter = value;
      this.getItems();
    })
  }

  ngAfterViewInit(): void {
    this.paginator.page
    .pipe(tap(() => this.getItems()))
    .subscribe();
    this.getItems();
  }

  getItem(id: number): void {
    this.boxService.get(id).subscribe(data => {
      this.box = data;
      this.getItems();
    });
  }

  getItems(){
    this.dataSource.loadItems(this.id, this.paginator.pageIndex, this.paginator.pageSize, this.itemFilter)
  }

  deleteItemClicked(id: number): void{
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: "Are you sure you would like to delete this item?"
    });

    dialogRef.afterClosed().pipe(first()).subscribe(result => {
      if(result){
        this.deleteItem(id);
      }
    });
  }

  deleteItem(id: number): void {
    this.itemService.delete(id).subscribe(() => {
      this.getItems();
    });
  }
}

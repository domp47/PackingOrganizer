import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BoxService } from 'src/app/Services/Box/box.service';
import { BaseChildEditComponent } from '../base-child-edit.component';

@Component({
  selector: 'app-item-edit',
  templateUrl: './item-edit.component.html',
  styleUrls: ['./item-edit.component.scss'],
})
export class ItemEditComponent
  extends BaseChildEditComponent
  implements OnInit
{
  name: string;

  constructor(
    activatedRoute: ActivatedRoute,
    private boxService: BoxService,
    private router: Router
  ) {
    super(activatedRoute);
    this.id = 0; //Remove if Edit is ever implemented
    this.name = '';
  }

  ngOnInit(): void {
    super.ngOnInit();
  }

  getItem(_id: number): void {
    // Not Implemented
  }

  cancel(): void {
    if (this.isNew()) {
      this.router.navigateByUrl('/boxes');
    } else {
      this.router.navigateByUrl('/box/' + this.parentId + '/view');
    }
  }

  save(): void {
    const obj: any = {};
    obj['name'] = this.name;
    obj['boxId'] = this.parentId;
    console.log(this.isNew());

    if (this.isNew()) {
      this.boxService.addItem(this.parentId, obj).subscribe((_data) => {
        this.router.navigateByUrl('box/' + this.parentId + '/view');
      });
    }
  }
}

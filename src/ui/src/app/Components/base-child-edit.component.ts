import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BaseEditComponent } from './base-edit.component';

@Component({
  template: '',
})
export abstract class BaseChildEditComponent
  extends BaseEditComponent
  implements OnInit
{
  parentId;

  constructor(private _route: ActivatedRoute) {
    super(_route);

    this.parentId = +this._route.snapshot.params['parentId'];
  }

  ngOnInit(): void {
    super.ngOnInit();
  }

  abstract getItem(id: number): void;
}

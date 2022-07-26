import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  template: '',
})
export abstract class BaseEditComponent implements OnInit {
  id: number;

  constructor(public route: ActivatedRoute) {
    this.id = +this.route.snapshot.params['id'];
  }

  ngOnInit(): void {
    if (!this.isNew()) {
      this.getItem(this.id);
    }
  }

  isNew(): boolean {
    return this.id === 0;
  }

  abstract getItem(id: number): void;
}

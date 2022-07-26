import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  template: '',
})
export abstract class BaseViewComponent implements OnInit {
  id: number;

  constructor(private route: ActivatedRoute) {
    this.id = +this.route.snapshot.params['id'];
  }

  ngOnInit(): void {
    this.getItem(this.id);
  }

  abstract getItem(id: number): void;
}

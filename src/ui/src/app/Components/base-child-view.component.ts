import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { BaseViewComponent } from "./base-view.component";

@Component({
    template: ''
})
export abstract class BaseChildViewComponent extends BaseViewComponent implements OnInit {

    parentId: number;

    constructor(private _route: ActivatedRoute) {
        super(_route);
        this.parentId = +this._route.snapshot.params["parentId"];
    }

    ngOnInit(): void {
        super.ngOnInit();
    }

    abstract getItem(id: number): void;
}
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BoxService } from 'src/app/Services/Box/box.service';
import { BaseEditComponent } from '../base-edit.component';

@Component({
  selector: 'app-box-edit',
  templateUrl: './box-edit.component.html',
  styleUrls: ['./box-edit.component.scss'],
})
export class BoxEditComponent extends BaseEditComponent implements OnInit {
  label: string;
  description: string;

  constructor(
    activatedRoute: ActivatedRoute,
    private boxService: BoxService,
    private router: Router
  ) {
    super(activatedRoute);

    this.label = '';
    this.description = '';
  }

  ngOnInit(): void {
    super.ngOnInit();
  }

  getItem(id: number): void {
    this.boxService.get(id).subscribe((data) => {
      this.label = data.label;
      this.description = data.description;
    });
  }

  cancel(): void {
    if (this.isNew()) {
      this.router.navigateByUrl('/boxes');
    } else {
      this.router.navigateByUrl('/box/' + this.id + '/view');
    }
  }

  save(): void {
    const obj: any = {};
    obj['label'] = this.label;
    obj['description'] = this.description;

    if (this.isNew()) {
      this.boxService.add(obj).subscribe((data) => {
        this.router.navigateByUrl('box/' + data.id + '/view');
      });
    } else {
      this.boxService.update(this.id, obj).subscribe((data) => {
        this.router.navigateByUrl('box/' + data.id + '/view');
      });
    }
  }
}

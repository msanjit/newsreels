import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit {

  accordionList:any;

  constructor() { 

    this.accordionList = [
      {
        id:"panel-1",
        title:"CNBC",
        description:"US President Donald Trump's administration has blocked Gordon Sondland, the US' Ambassador to the EU, from testifying in Trump's impeachment inquiry. Text messages have shown Sondland and other officials discussing military aid to Ukraine and investigation of the 2016 presidential election. Trump's impeachment inquiry was sparked by his phone call with Ukrainian President Volodymyr Zelenskyy",
        isExpanded:false
      },{
        id:"panel-2",
        title:"BUSINESS STANDARD",
        description:"Maruti Suzuki reduced its production by 17.5% in September, making it the eighth straight month the country's largest carmaker lowered its output. The company produced a total of 1,32,199 units in September as against 1,60,219 units the same month last year. Maruti Suzuki had cut its production by 34% to 1,11,370 units in August.",
        isExpanded:false
      },{
        id:"panel-3",
        title:"FINANCIAL EXPRESS",
        description:"The fund flows from banks and non-banks to the commercial sector declined by 88% till mid-September this financial year, data released by the RBI showed. Such flows fell to ₹90,995 crore from ₹7.36 lakh crore in the same period last year. The RBI said the decline was partly due to risk aversion and partly due to a slowdown in demand.",
        isExpanded:true
      },
    ]

  }

  ngOnInit() {
  }

  panelOpenState = false;

  fileContent: string = '';
  fileName : string = '';

  //public onFileInput(fileList: FileList): void {
    public onFileInput(fileInput: Event): void {
      let target= event.target as HTMLInputElement;
      //let file = fileInput.target.files[0];
      let file: File = (target.files as FileList)[0];
      let fileName = file.name;
      let fileReader: FileReader = new FileReader();
      let self = this;
      self.fileName = fileName;
      fileReader.onloadend = function(x) {
        self.fileContent = fileReader.result;
        self.accordionList.push({
          //id:"panel-4",
          title:fileName.split('.')[0],
          description:self.fileContent,
          isExpanded:false
        });
      }
      fileReader.readAsText(file);

      
    }

}

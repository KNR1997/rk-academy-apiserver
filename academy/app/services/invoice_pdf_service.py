from io import BytesIO

from django.template.loader import render_to_string

from weasyprint import HTML


class InvoicePdfService:

    @classmethod
    def generate(cls, invoice):

        html = render_to_string(
            "invoices/invoice.html",
            {
                "invoice": invoice
            }
        )

        pdf_file = BytesIO()

        HTML(
            string=html
        ).write_pdf(
            target=pdf_file
        )

        pdf_file.seek(0)

        return pdf_file

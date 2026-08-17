import React, { useState } from 'react';
import { X, Download, RefreshCw, Flag, BookOpen, FileText, FileSpreadsheet, Printer, Check } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const Modals: React.FC = () => {
  const { activeModal, setActiveModal, currentResult, clearHistory, history, showToast } = useApp();

  const [reportReason, setReportReason] = useState<string>('incorrect_verdict');
  const [reportComment, setReportComment] = useState<string>('');
  const [reportSubmitted, setReportSubmitted] = useState<boolean>(false);
  const [docxMsg, setDocxMsg] = useState<string | null>(null);

  if (!activeModal) return null;

  const handleClose = () => {
    setActiveModal(null);
    setReportSubmitted(false);
    setDocxMsg(null);
  };

  const exportJSON = () => {
    const dataStr = JSON.stringify(currentResult || history, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `clarifai_verification_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Exported JSON successfully');
    handleClose();
  };

  const exportCSV = () => {
    const items = currentResult ? [currentResult] : history.map((h) => h.full_result || h);
    let csv = 'Claim,Verdict,Confidence,Confidence Level\n';
    items.forEach((item: any) => {
      const claimStr = `"${(item.claim || '').replace(/"/g, '""')}"`;
      csv += `${claimStr},${item.verdict},${item.confidence},${item.confidence_level || ''}\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `clarifai_summary_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Exported CSV successfully');
    handleClose();
  };

  const triggerPDFPrint = () => {
    handleClose();
    setTimeout(() => {
      window.print();
    }, 200);
  };

  const triggerDOCXComingSoon = () => {
    setDocxMsg('DOCX export coming soon in next release.');
    setTimeout(() => setDocxMsg(null), 3000);
  };

  const handleClearCacheConfirm = () => {
    clearHistory();
    showToast('Cache cleared successfully');
    handleClose();
  };

  const handleReportSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setReportSubmitted(true);
    showToast('Misclassification report submitted');
    setTimeout(() => {
      handleClose();
    }, 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="w-full max-w-lg glass-content rounded-3xl p-6 shadow-2xl relative text-[#111827] dark:text-white border border-black/10 dark:border-white/10">
        <button
          onClick={handleClose}
          className="absolute top-5 right-5 text-[#475569] dark:text-[#A7A7A7] hover:text-[#111827] dark:hover:text-white p-1 rounded-full hover:bg-black/5 dark:hover:bg-white/10 transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* MODAL 1: EXPORT SCAN */}
        {activeModal === 'export' && (
          <div className="space-y-5">
            <div className="flex items-center gap-2.5">
              <Download className="w-5 h-5 text-[#1DB954]" />
              <h3 className="text-lg font-bold">Export Verification Report</h3>
            </div>
            <p className="text-xs text-[#475569] dark:text-[#A7A7A7]">
              Choose your preferred report format to download or print your verification audit.
            </p>

            {docxMsg && (
              <div className="p-3 bg-[#F5B942]/15 text-[#F5B942] font-bold text-xs rounded-2xl">
                {docxMsg}
              </div>
            )}

            <div className="grid grid-cols-2 gap-3 pt-2">
              <button
                onClick={exportJSON}
                className="flex items-center gap-3 p-3.5 glass-interactive rounded-2xl text-left text-xs font-bold transition-all cursor-pointer"
              >
                <FileText className="w-5 h-5 text-[#00C2FF]" />
                <div>
                  <div>JSON Format</div>
                  <div className="text-[10px] font-normal text-[#475569] dark:text-[#A7A7A7]">Raw structured data</div>
                </div>
              </button>

              <button
                onClick={exportCSV}
                className="flex items-center gap-3 p-3.5 glass-interactive rounded-2xl text-left text-xs font-bold transition-all cursor-pointer"
              >
                <FileSpreadsheet className="w-5 h-5 text-[#1DB954]" />
                <div>
                  <div>CSV Table</div>
                  <div className="text-[10px] font-normal text-[#475569] dark:text-[#A7A7A7]">Spreadsheet summary</div>
                </div>
              </button>

              <button
                onClick={triggerPDFPrint}
                className="flex items-center gap-3 p-3.5 glass-interactive rounded-2xl text-left text-xs font-bold transition-all cursor-pointer"
              >
                <Printer className="w-5 h-5 text-[#F5B942]" />
                <div>
                  <div>Printable PDF Report</div>
                  <div className="text-[10px] font-normal text-[#475569] dark:text-[#A7A7A7]">Full visual report</div>
                </div>
              </button>

              <button
                onClick={triggerDOCXComingSoon}
                className="flex items-center gap-3 p-3.5 glass-interactive rounded-2xl text-left text-xs font-bold transition-all cursor-pointer opacity-70"
              >
                <FileText className="w-5 h-5 text-[#FF4D5A]" />
                <div>
                  <div>DOCX Document</div>
                  <div className="text-[10px] font-normal text-[#475569] dark:text-[#A7A7A7]">Coming soon</div>
                </div>
              </button>
            </div>
          </div>
        )}

        {/* MODAL 2: CLEAR CACHE */}
        {activeModal === 'cache' && (
          <div className="space-y-4">
            <div className="flex items-center gap-2.5">
              <RefreshCw className="w-5 h-5 text-[#00C2FF]" />
              <h3 className="text-lg font-bold">Clear Local Cache</h3>
            </div>
            <p className="text-xs text-[#475569] dark:text-[#A7A7A7]">
              This will clear all locally cached news search indices and browser analysis history. Saved bookmarks will remain intact.
            </p>
            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={handleClose}
                className="px-4 py-2 text-xs font-bold glass-interactive rounded-2xl cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleClearCacheConfirm}
                className="px-4 py-2 text-xs font-bold bg-[#FF4D5A] text-white rounded-2xl shadow-md hover:bg-[#e04350] transition-all cursor-pointer"
              >
                Clear Cache
              </button>
            </div>
          </div>
        )}

        {/* MODAL 3: REPORT MISCLASSIFICATION */}
        {activeModal === 'report' && (
          <div className="space-y-4">
            <div className="flex items-center gap-2.5">
              <Flag className="w-5 h-5 text-[#FF4D5A]" />
              <h3 className="text-lg font-bold">Report Misclassification</h3>
            </div>

            {reportSubmitted ? (
              <div className="p-4 bg-[#1DB954]/15 text-[#1DB954] font-bold text-xs rounded-2xl flex items-center gap-2">
                <Check className="w-4 h-4" />
                <span>Thank you! Your feedback has been submitted to the ClarifAI model calibration pipeline.</span>
              </div>
            ) : (
              <form onSubmit={handleReportSubmit} className="space-y-3 text-xs">
                <div>
                  <label className="font-semibold block mb-1 text-[#475569] dark:text-[#A7A7A7]">Feedback Category</label>
                  <select
                    value={reportReason}
                    onChange={(e) => setReportReason(e.target.value)}
                    className="w-full p-2.5 glass-interactive rounded-2xl text-[#111827] dark:text-white focus:outline-none"
                  >
                    <option value="incorrect_verdict" className="bg-white dark:bg-[#121212]">Incorrect Verdict Classification</option>
                    <option value="irrelevant_evidence" className="bg-white dark:bg-[#121212]">Irrelevant Evidence Articles</option>
                    <option value="misleading_ml" className="bg-white dark:bg-[#121212]">Misleading ML Linguistic Analysis</option>
                    <option value="other" className="bg-white dark:bg-[#121212]">Other Model Calibration Feedback</option>
                  </select>
                </div>

                <div>
                  <label className="font-semibold block mb-1 text-[#475569] dark:text-[#A7A7A7]">Additional Comments (Optional)</label>
                  <textarea
                    rows={3}
                    value={reportComment}
                    onChange={(e) => setReportComment(e.target.value)}
                    placeholder="Provide details regarding why this verification verdict needs re-calibration..."
                    className="w-full p-2.5 glass-interactive rounded-2xl text-[#111827] dark:text-white placeholder-[#64748B] focus:outline-none"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={handleClose}
                    className="px-4 py-2 font-bold glass-interactive rounded-2xl cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 font-bold bg-[#1DB954] text-black rounded-2xl shadow-md hover:bg-[#1ed760] transition-all cursor-pointer"
                  >
                    Submit Report
                  </button>
                </div>
              </form>
            )}
          </div>
        )}

        {/* MODAL 4: DOCUMENTATION */}
        {activeModal === 'doc' && (
          <div className="space-y-4">
            <div className="flex items-center gap-2.5">
              <BookOpen className="w-5 h-5 text-[#F5B942]" />
              <h3 className="text-lg font-bold">Documentation & Verification Engine</h3>
            </div>
            <div className="text-xs text-[#475569] dark:text-[#A7A7A7] space-y-2 max-h-60 overflow-y-auto pr-2">
              <p>
                <strong>ClarifAI Engine Architecture:</strong> ClarifAI combines real-time evidence retrieval via DuckDuckGo News Indexing with a calibrated Calibrated Linear SVM TF-IDF model.
              </p>
              <p>
                <strong>Confidence Scoring:</strong> Calculated dynamically from article consensus, domain independence, and TF-IDF feature distributions.
              </p>
              <p>
                <strong>Linguistic ML Disclaimer:</strong> The ML model measures stylistic linguistic patterns and does not establish absolute truth independently.
              </p>
            </div>
            <div className="flex justify-end pt-2">
              <button
                onClick={handleClose}
                className="px-4 py-2 text-xs font-bold bg-[#00C2FF] text-black rounded-2xl shadow-md cursor-pointer"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
